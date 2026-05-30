from . import options, consts
from .os_tools import get_os
import pygame

_os = get_os()

if _os == consts.OS_LINUX:
    from dasbus.connection import SessionMessageBus
    _bus = SessionMessageBus()
    _orca = _bus.get_proxy("org.gnome.Orca1.Service", "/org/gnome/Orca1/Service")
    linux_speaker = _bus.get_proxy("org.gnome.Orca1.Service", "/org/gnome/Orca1/Service/SpeechManager")
    if options.get("linux_speech_rate") is not None:
        linux_speaker.Rate = int(options.get("linux_speech_rate"))
    if options.get("linux_speech_pitch") is not None:
        linux_speaker.Pitch = float(options.get("linux_speech_pitch"))
    if options.get("linux_speech_volume") is not None:
        linux_speaker.Volume = float(options.get("linux_speech_volume"))
else:
    from accessible_output2 import outputs
    _ao2 = outputs.auto.Auto()

history = []  # should only be used for viewing on the screen, might contain diffrant things than what's spoken.


def speak(text, interupt=True, store_in_history=True, id=None, silent=False):
    if options.get("mute_speech_on_focus_loss", False) and not pygame.key.get_focused():
        silent = True
    if id is not None:
        for item in history:
            if item[1] == id:
                history.remove(item)
    if store_in_history:
        history.append((text, id))
    if not silent:
        if _os == consts.OS_LINUX:
            if interupt:
                linux_speaker.InterruptSpeech(False)
            _orca.PresentMessage(text)
        else:
            _ao2.output(text, interupt)
