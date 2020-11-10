# webscrapers
Different web scrapers built using python and selenium

# Usage

* `google_question_answering.py`: Retrieves responses for a question using Google's Question Answering system

```bash
python google_question_answering.py --question "whatsapp acquired by"
python google_question_answering.py --question "us population"
python google_question_answering.py --question "fastest plane speed"
python google_question_answering.py --question "worldcup 2022 country" "amazon ticker cost" "github acquired by"
```

* `oaca.py`: Retrieves Tunisia's today flights

```bash
python3 -m oaca
python3 -m oaca --airport tunis --out flights_03_11_2020.csv
```

* `amazon_india.py`: Add product from amazon india to wish list

```bash
python3 -m amazon_india --username "username" --password "password" --product "iphone 7"
python3 -m amazon_india --username "username" --password "password" --product "iphone 7" --wish-list "My wish list"
```