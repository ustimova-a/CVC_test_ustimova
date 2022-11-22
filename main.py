from bs4 import BeautifulSoup as bs
import requests
import time
import argparse


def get_jokes():
    with open('jokes.txt', 'w') as file:
        result_list = []
        parser = argparse.ArgumentParser()
        parser.add_argument('--start_id', type=int, required=True)
        parser.add_argument('--end_id', type=int, required=True)
        args = parser.parse_args()
        for id in range(args.start_id, args.end_id):
            payload = {'a': id}
            r = requests.get("https://anek.ws/anekdot.php", params=payload)
            soup = bs(r.text, "html.parser")
            joke = soup.find(id='anek').get_text()
            result_list.append(joke)
            time.sleep(0.5)

        file.write('\n\n'.join(result_list))

    return file


if __name__ == "__main__":
    get_jokes()