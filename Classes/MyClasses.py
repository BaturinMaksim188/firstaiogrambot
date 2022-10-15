from aiogram.dispatcher.filters.state import State, StatesGroup


# Class for getting the proposed post
class States(StatesGroup):
    Text = State()
    TextVerification = State()
    PictureQuestion = State()
    Picture = State()
    Last = State()


# Class for the "/send" command
class StateToSend(StatesGroup):
    TakeMessage = State()


# Class for unloading records from the database
class StateToAppend(StatesGroup):
    WelcomeState = State()
    CyclicState = State()
    ProcessingState = State()
    PauseState = State()