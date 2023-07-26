import streamlit as st
import pandas as pd
from datetime import datetime

def main():
    #writing chart title 
    st.title('Monthly sales analysis')
    st.write('')
    
    #creating data frame for monthly sales
    df = pd.DataFrame({'Month' : ['Jan', 'Feb', 'Mar','Apr', 'May','Jun'],
                        'Sales': [1000, 2000, 1540, 1700,1320, 1120]})
    
    #rendering dataframe on the left and chart on the right panel
    col1, col2 = st.columns([1,3])
    with col1:
        st.dataframe(df)
    with col2:
        st.bar_chart(df,x='Month',y='Sales')
        
        
    #Comment section   
    
    df_comment = None
    
    #check if 'comment' is not existed in session state then load csv and store in the session state
    if 'comment' not in st.session_state:
        df_comment = pd.read_csv('comment.csv')
        st.session_state.comment = df_comment
    #or if 'commment' is existed then restore the csv comment from the session state 
    else:
        df_comment = st.session_state.comment
    
    if 'just_submitted' not in st.session_state:
        st.session_state.just_submitted = False
    
    #rendering comment section
    with st.expander('💬 Open comment section'):
        #formating the output of comments and replies
        COMMENT_TEMPLATE = '**{}** - {}\n\n|&nbsp;&nbsp;&nbsp;&nbsp;{}'
        REPLY_TEMPLATE = '\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;**Reply**: {} - {}'
        #iterate each comment in the dataset and render it on the web page 
        for _, comment in df_comment.iterrows():
            str = COMMENT_TEMPLATE.format(comment['Name'],comment['Date'],comment['Comment']) +\
                  ('' if pd.isnull(comment['Reply']) else REPLY_TEMPLATE.format(comment['Reply'],comment['Reply Date']))
            st.markdown(str)
        
        if st.session_state.just_submitted:
            st.success("☝️ Your comment was successfully submitted.") 
            st.session_state.just_submitted = False
    
        st.write('***Add your comment***')
        
        with st.form('comment_section', clear_on_submit=True):
            #adding text inputs for name and comment, and a submit button
            name = st.text_input('Name')
            comment = st.text_area('Comment')
            submit = st.form_submit_button('Submit')
                  
            if submit and name!= '' and comment!='':
                #getting server local time
                date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
                #adding new comment to the comment dataframe
                df_comment = df_comment.append({'Name':name,'Comment':comment,'Date':date}, ignore_index=True)
                #overwriting the dataframe into csv comment file
                df_comment.to_csv('comment.csv',index=False)
                #update the session state to flag a new comment is justed added
                if st.session_state.just_submitted == False:
                    st.session_state.just_submitted = True
                
                #delete the session state to force to refresh all comments
                del st.session_state.comment
                st.experimental_rerun()
    
if __name__=='__main__':
    main()