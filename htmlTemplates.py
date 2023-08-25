css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e;
    flex-direction: row-reverse;
}
.chat-message.user > .message{
direction:rtl;
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}

.css-zt5igj{
    direction:rtl;
}
.css-pb6fr7{
direction:rtl;
}
.css-1qg05tj{
direction:rtl;
font-size:18px;
}
.css-cio0dv{
display:none;
}
.stDeployButton{
display:none;
}

#MainMenu{
display: none;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://img.freepik.com/free-vector/illustration-businessman_53876-5856.jpg?t=st=1692995747~exp=1692996347~hmac=6292effb59d639613644df3e7c2de29add64441865752beeb4a52fdab30f3193" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://img.freepik.com/free-psd/3d-icon-social-media-app_23-2150049569.jpg?w=740&t=st=1692996631~exp=1692997231~hmac=68b4f502212f59bab141adc00c263fa9e7ddb03406a57f84c895747da166ec9d">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''