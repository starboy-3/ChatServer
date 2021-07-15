from ast import literal_eval
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Chat, Contact, Message


def user_exists(username):
    user = User.objects.filter(username=username).first()
    return 0 if user is None else user.id


def add_users_to_chat(chat, users):
    for userId in users:
        user = User.objects.filter(id=userId).first()
        userExistsInChat = Contact.objects.filter(chat=chat, user=userId).first()

        if user is not None and userExistsInChat is None:
            chatUserObj = Contact.objects.create(chat=chat, user=user)
            chatUserObj.save()


def chat_exists(chatName):
    chat = Chat.objects.filter(name=chatName).first()
    return 0 if chat is None else chat.id


def add_user(username):
    userExists = user_exists(username)
    if not userExists:
        try:
            userObj = User.objects.create(username=username,
                                          created_at=timezone.now())
            userObj.save()
            userId = User.objects.filter(username=username).first().id
            return {"userId": userId, "status": 200}
        except:
            return {"userId": None, "status": 400}
    return {"userId": userExists, "status": 200}


def add_chat(chatName, users):
    chatExists = chat_exists(chatName)
    if not chatExists:
        try:
            chatObj = Chat.objects.create(name=chatName,
                                          created_at=timezone.now())
            chatObj.save()
            chat = Chat.objects.filter(name=chatName).first()
            add_users_to_chat(chat, users)

            return {"chatId": chat.id, "status": 200}
        except:
            return {"chatId": None, "status": 400
                    }
    chat = Chat.objects.filter(name=chatName).first()
    add_users_to_chat(chat, users)
    return {"chatId": chatExists, "status": 200}


def add_message(chatId, userId, text):
    chat = Chat.objects.filter(id=chatId).first()
    author = User.objects.filter(id=userId).first()

    messageObj = Message.objects.create(chat=chat,
                                        author=author,
                                        text=text,
                                        created_at=timezone.now())
    messageObj.save()


def get_chats(userId):
    chatsUserDB = Contact.objects.filter(user=userId)
    chats = []

    for chatUserDB in chatsUserDB:
        chatMessages = Message.objects.filter(chat=chatUserDB.chat).order_by('created_at').reverse()
        for message in chatMessages:
            chats.append([chatUserDB.chat, message.created_at.created_at.now().strftime("%Y-%m-%d %H:%M:%S")])
            break


def get_messages(chatId):
    messagesDB = Message.objects.filter(chat=chatId).order_by('created_at').reverse()
    messages = []

    for message in messagesDB:
        messages.append([message.chat.name, message.author.username, message.text,
                         message.created_at.now().strftime("%Y-%m-%d %H:%M:%S")])
    return


@csrf_exempt
def addUser(request):
    body = request.body
    body = body.decode("utf-8")
    data = literal_eval(body)

    if 'username' in data:
        user = add_user(data['username'])
        return HttpResponse(user["userId"], status=user["status"])
    return HttpResponse(status=400)


@csrf_exempt
def addChat(request):
    body = request.body
    body = body.decode("utf-8")
    data = literal_eval(body)

    if 'name' in data and 'users' in data and data['users'] != []:
        chat = add_chat(data['name'], data['users'])
        return HttpResponse(chat["chatId"], status=chat["status"])
    return HttpResponse(status=400)


@csrf_exempt
def addMessage(request):
    body = request.body
    body = body.decode("utf-8")
    data = literal_eval(body)

    if 'chat' in data and 'author' in data and 'text' in data:
        try:
            chatExists = Chat.objects.filter(id=data['chat']).first()
            authorExists = User.objects.filter(id=data['author']).first()
            add_message(data['chat'], data['author'], data['text'])
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=400)
    return HttpResponse(status=400)


@csrf_exempt
def getChats(request):
    body = request.body
    body = body.decode("utf-8")
    data = literal_eval(body)

    if 'user' in data:
        get_chats(data['user'])
        return HttpResponse(status=200)
    return HttpResponse(status=400)


@csrf_exempt
def getMessages(request):
    body = request.body
    body = body.decode("utf-8")
    data = literal_eval(body)

    if 'chat' in data:
        get_messages(data['chat'])
        return HttpResponse(status=200)
    return HttpResponse(status=400)
