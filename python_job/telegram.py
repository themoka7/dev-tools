import os
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

# 텔레그램 설정
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_TREND_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")



def send_telegram_message(message):
    """텔레그램으로 메시지 전송"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[텔레그램] 봇 토큰 또는 채팅 ID가 설정되지 않았습니다.")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print("[텔레그램] 메시지 전송 완료")
            return True
        else:
            print(f"[텔레그램] 전송 실패: {response.status_code}")
            return False
    except Exception as e:
        print(f"[텔레그램] 오류: {e}")
        return False







# 텔레그램 메시지 작성 (테스트)
def test_telegram():
    telegram_message = "🔥 <b>Google Trends Update</b>\n"
    telegram_message += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    telegram_message += f"✅ 텔레그램 연결 테스트\n"
    
    return send_telegram_message(telegram_message)


if __name__ == "__main__":
    # 테스트 실행
    test_telegram()

