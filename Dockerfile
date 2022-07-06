# Install requirements
RUN pip3 install -U -r requirements.txt

CMD ["python3", "-m", "TgBot"]
