from pathlib import Path
import json

p = Path('build-src/watchface/index.js')
s = p.read_text(encoding='utf-8')
marker = '// BALANCE2_CLOCK_TAP_ZONES'
if marker not in s:
    candidates = ['init_view() {', 'build() {', 'onInit() {']
    start = -1
    needle = None
    for candidate in candidates:
        start = s.find(candidate)
        if start >= 0:
            needle = candidate
            break
    if start < 0:
        raise SystemExit('No suitable watchface init method found')
    brace = s.find('{', start)
    depth = 0
    end = None
    for i in range(brace, len(s)):
        if s[i] == '{':
            depth += 1
        elif s[i] == '}':
            depth -= 1
            if depth == 0:
                end = i
                break
    if end is None:
        raise SystemExit(f'{needle} closing brace not found')
    block = '''\n    // BALANCE2_CLOCK_TAP_ZONES\n    hmUI.createWidget(hmUI.widget.IMG_CLICK, { x: 62, y: 174, w: 148, h: 98, type: hmUI.data_type.ALARM_CLOCK, show_level: hmUI.show_level.ONLY_NORMAL })\n    hmUI.createWidget(hmUI.widget.IMG_CLICK, { x: 256, y: 174, w: 148, h: 98, type: hmUI.data_type.COUNT_DOWN, show_level: hmUI.show_level.ONLY_NORMAL })\n    hmUI.createWidget(hmUI.widget.IMG_CLICK, { x: 202, y: 254, w: 76, h: 58, type: hmUI.data_type.STOP_WATCH, show_level: hmUI.show_level.ONLY_NORMAL })\n'''
    s = s[:end] + block + s[end:]
    p.write_text(s, encoding='utf-8')

app = Path('build-src/app.json')
data = json.loads(app.read_text(encoding='utf-8'))
data['app']['version']['code'] = 2
data['app']['version']['name'] = '1.1'
app.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
