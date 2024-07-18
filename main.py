from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import random
from fastapi.middleware.cors import CORSMiddleware

# 발급받은 API 키 설정
OPENAI_API_KEY = "sk-proj-Zs9GIdC6EJHugKsJZxfRT3BlbkFJUMC233ocSoYPq6SexXJi"

# OpenAI API 키 인증
openai.api_key = OPENAI_API_KEY



# 모델 - GPT 3.5 Turbo 선택
model = "gpt-3.5-turbo"

# FastAPI 인스턴스 생성
app = FastAPI()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # 또는 "GET", "POST"와 같이 특정 메소드만 허용할 수 있습니다.
    allow_headers=["*"],  # 또는 "Content-Type", "Authorization"와 같이 특정 헤더만 허용할 수 있습니다.
)

# 요청 데이터 모델 정의
class Query(BaseModel):
    question: str

# 주식 추천 리스트
stock_recommendations = [
    "보겸", "감스트", "조재원", "준우", "피지컬갤러리", "장삐쭈", "곽튜브", "빠니보틀", 
    "가재맨", "쯔양", "파뿌리", "핫도그", "워크맨", "혜안", "핫소스", "진용진", "허팝", 
    "히밥", "올리버쌤", "보물섬", "김블루", "말왕", "피식대학", "고몽", "미미미누", "이재명", 
    "냥뇽녕냥", "쵸단", "너덜트", "이상호", "대덕소마고", "뷰티풀너드", "올리버쌤", 
    "사우스 코리안 파크", "총몇명", "horese-kingtv", "꼰대희", "장지수", "부산소마고", 
    "대구소마고", "광주소마고", "지무비", "너진똑", "침착맨", "주둥이방송", "마젠타", "윤석열", "디에프(딩고프리스타일)",
    "오킹", "보다 BODA", "스토리", "빠더너스", "LG 트윈스", "스케치 코미디"
]

# 금지어 리스트
prohibited_keywords = ["야한", "음란한", "성적인", "섹스", "포르노"]  # 필요한 키워드 추가 가능

# 운세 문장 리스트
fortune_responses = [
    "오늘은 정말 완벽합니다!",
    "오늘 운세가 좋지 않네요ㅠㅠ",
    "당신의 감을 믿으세요!",
    "지금이 기회입니다."
]


# 금지어가 포함되어 있는지 확인하는 함수 정의
def contains_prohibited_content(text: str) -> bool:
    return any(keyword in text for keyword in prohibited_keywords)

# 루트 엔드포인트 정의
@app.get("/")
def read_root():
    return {"message": "Welcome to the ChatGPT API powered by FastAPI"}

# 질문 엔드포인트 정의
@app.post("/ask")
async def ask_question(query: Query):
    # "오늘의 주식을 추천해줘"라는 질문인지 확인
    if query.question == "오늘의 주식 추천~":
        recommendation = random.choice(stock_recommendations)
        return {"answer": "오늘의 주식은 {}입니다".format(recommendation)}
    
     # "어떤 분야의 유튜버가 있나요?"라는 질문인지 확인
    if query.question == "어떤 분야의 유튜버가 있나요?":
        return {
            "answer": "먹방, 챌린지, 소통, 여행, 만화, 정치, 노래, 코미디, 고민상담, 영화리뷰, 드라마, 운동, 실험 등등 있습니다"
        }
    
    
    if query.question == "몇명의 유튜버가 있나요?":
        return {
            "answer": "54명의 유튜버가 있습니다!"
        }
    
    # "오늘의 운세를 말해줘"라는 질문인지 확인
    if query.question == "오늘의 운세를 말해줘":
        fortune = random.choice(fortune_responses)
        return {"answer": fortune}

    # 금지어가 포함되어 있는지 확인
    if contains_prohibited_content(query.question):
        return {"answer": "그런 질문은 받을 수 없습니다"}

    # 메시지 설정하기
    messages = [{
        "role": "system",
        "content": "You are a helpful assistant."
    }, {
        "role": "user",
        "content": query.question
    }]

    try:
        # ChatGPT API 호출하기
        response = openai.ChatCompletion.create(model=model, messages=messages)
        answer = response['choices'][0]['message']['content']
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 애플리케이션 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
