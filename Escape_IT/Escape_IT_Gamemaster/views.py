import sys
import os

from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from django.http import FileResponse
from django.shortcuts import render


def home(request):
    context = {
        'title': 'Gamemaster home'
    }

    if request.method == 'POST':
        text = request.POST.get('text_to_convert')
        if text:
            session = Session(profile_name="default")
            polly_client = session.client('polly')

            try:
                response = polly_client.synthesize_speech(
                    Text=text,
                    VoiceId='Brian',
                    OutputFormat='mp3')
            except(BotoCoreError, ClientError) as error:
                print(error)
                sys.exit(-1)

            file_path = 'E:/Unity/Projects/Escape_IT/Assets/Sound effects/speech.mp3'

            if os.path.exists(file_path):
                os.remove(file_path)

            with open(file_path, 'wb') as file:
                file.write(response['AudioStream'].read())


    return render(request, 'Escape_IT_Gamemaster/home.html', context)
