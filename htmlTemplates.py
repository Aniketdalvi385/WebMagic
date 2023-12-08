css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 1rem; margin-bottom: 1rem; display: flex;
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
    width: 15%
}
.chat-message .avatar img {
    max-width: 78px;
    max-height: 78px;
    border-radius: 50%;
    object-fit: cover;
}
.chat-message .message {
    width: 85%;
    padding: 0 1.5rem;
    color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://img.freepik.com/free-vector/cute-robot-wearing-hat-flying-cartoon-vector-icon-illustration-science-technology-icon-isolated_138676-5186.jpg?w=826&t=st=1701148430~exp=1701149030~hmac=59c7195aa80397aceffa10af9c5bcbd679c0ce1fa66fdde74674b6d546e6bdff" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit= cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://img.freepik.com/free-vector/isolated-young-handsome-man-different-poses-white-background-illustration_632498-859.jpg?w=826&t=st=1701147647~exp=1701148247~hmac=e5c2c6f6a03237af47d583c7e4a7b34d624ef5ce6e6fa94ae24f42efa659878d">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''