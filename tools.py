import time, json, os

def delay_seconds(seconds):
    time.sleep(seconds)
    return None

def delay_microseconds(microseconds):
    # Xác định thời điểm bắt đầu
    start_time = time.perf_counter_ns()

    # Tính thời điểm kết thúc dự kiến
    end_time = start_time + microseconds * 1000  # Chuyển đổi từ microseconds thành nanoseconds

    # Vòng lặp chờ với độ phân giải 1 nano seconds
    while time.perf_counter_ns() < end_time: pass
    return None

 
def load_json(path='./config.json', encoding='utf-8'):
    if os.path.exists(path):
        with open(path, 'r', encoding=encoding) as json_file:
            return json.load(json_file)
    else:
        raise RuntimeError('File error')
    

def save_json(path='./config.json', data=None, encoding='utf-8'):
    with open(path, 'w', encoding=encoding) as json_file:
        json.dump(data, json_file, indent=4)
    return True

    