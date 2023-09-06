# StockPrice-App

### Stock price data + LLM 

In this data application an architecture is developed to fetch stock price data from wikipedia (via webscraping) or yfinance python library (near real-time). This app uses Langchain & OpenAI LLM model to provide chat capability on dataset. Users can ask data related questions on loaded stock price data for any stock (eg. - Which stock symbols saw more than 1% growth today?)

Link to code - [Stock price app](https://github.com/iamjaspreetsingh/StockPrice-App/blob/master/app_stockprice.py)

<img width="1440" alt="Screenshot 2023-09-06 at 8 42 56 PM" src="https://github.com/iamjaspreetsingh/StockPrice-App/assets/30948046/e410384c-1a86-4591-adc0-0fbe0f7e3ae6">


### Real time data integration 
In this data app, an architecture where streaming data from Confluent Kafka is fetched into Timeplus creating real-time streams. Timeplus gives us SQL capabilities on top of realtime data. Timeplus is integrated with Streamlit library in Python to create Tables in data app that can be seen getting updated in real-time. 

Link to code - [Real time app](https://github.com/iamjaspreetsingh/StockPrice-App/blob/master/real_time_app.py)


<img width="1432" alt="Screenshot 2023-09-06 at 9 23 13 PM" src="https://github.com/iamjaspreetsingh/StockPrice-App/assets/30948046/729645c7-8b31-4e51-9e4f-270453b32c6c">
<img width="1398" alt="Screenshot 2023-09-06 at 9 23 47 PM" src="https://github.com/iamjaspreetsingh/StockPrice-App/assets/30948046/489c6152-f78f-4624-9f74-cbf02cd29d4f">
