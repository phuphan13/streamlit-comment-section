import streamlit as st
import pandas as pd
from datetime import datetime

def main():
    
    st.title('Monthly sales analysis')
    st.write('')
    
    df = pd.DataFrame({'Month' : ['Jan', 'Feb', 'Mar','Apr', 'May','Jun'],
                        'Sales': [1000, 2000, 1540, 1700,1320, 1120]})
    
    col1, col2 = st.columns([1,3])
    
    with col1:
        st.dataframe(df)
        
    with col2:
        st.bar_chart(df,x='Month',y='Sales')
        
        
    #Creating the comment section    
    
    df_comment = None
    
    #Loading comments file
    if 'comment' not in st.session_state:
        df_comment = pd.read_csv('comment.csv')
        st.session_state.comment = df_comment
    else:
        df_comment = st.session_state.comment
    
    if 'just_posted' not in st.session_state:
        st.session_state.just_posted = False
    
    #rendering comment section
    with st.expander('💬 Open comments'):
       
        COMMENT_TEMPLATE = '**{}** - {}\n\n|&nbsp;&nbsp;&nbsp;&nbsp;{}'
        REPLY_TEMPLATE = '\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;**Reply**: {} - {}'
        
        for _, comment in df_comment.iterrows():
            str = COMMENT_TEMPLATE.format(comment['Name'],comment['Date'],comment['Comment']) +\
                  ('' if pd.isnull(comment['Reply']) else REPLY_TEMPLATE.format(comment['Reply'],comment['Reply Date']))
            st.markdown(str)
        
        if st.session_state.just_posted:
            st.success("☝️ Your comment was successfully posted.") 
            st.session_state.just_posted = False
        
        #adding new comments
        st.write('***Add your own comment***')
        
        with st.form('comment_section', clear_on_submit=True):
            name = st.text_input('Name')
            comment = st.text_area('Comment')
            submit = st.form_submit_button('Add comment')
                  
            if submit and name!= '' and comment!='':
                date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
                df_comment = df_comment.append({'Name':name,'Comment':comment,'Date':date}, ignore_index=True)
                df_comment.to_csv('comment.csv',index=False)
                if st.session_state.just_posted == False:
                    st.session_state.just_posted = True
                
                #delete the state and force to refresh the comment - use callback function
                del st.session_state.comment
                st.experimental_rerun()
    
if __name__=='__main__':
    main()