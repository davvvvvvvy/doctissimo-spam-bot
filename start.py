from src.doctissimo import doing

file = open('threads.txt', 'r')
lines = file.read().split('\n')
file.close()

titles = []
descs = []

link = open('link.txt', 'r')
link = link.read()

for line in lines:
    line = line.split('|')
    titles.append(line[0])
    descs.append(line[1].replace(f'{link}', f'[url={link}][b]{link}[/b][/url]')
                .replace(f'Viagra', f'[url={link}][b]Viagra[/b][/url]')
                .replace(f'viagra', f'[url={link}][b]Viagra[/b][/url]')
                .replace(f'Cialis', f'[url={link}][b]Cialis[/b][/url]')
                .replace(f'cialis', f'[url={link}][b]Cialis[/b][/url]')
                .replace(f'Kamagra', f'[url={link}][b]Kamagra[/b][/url]')
                .replace(f'kamagra', f'[url={link}][b]Kamagra[/b][/url]')
                .replace(f'KAMAGRA', f'[url={link}][b]Kamagra[/b][/url]'))

import time

while True:
    for j in range(0, 4):
        for i in range(0, 10):
            try:
                doing(titles[i], descs[i])
            except Exception as e:
                print(e)
    time.sleep(3600 * 3)