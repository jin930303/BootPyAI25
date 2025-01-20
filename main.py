from fastapi import FastAPI     # 파이썬 웹 개발 api
from pydantic import BaseModel  # 유효성 검사용   파이단틱
from starlette.middleware.base import BaseHTTPMiddleware
# 요청과 응답사이에 특정 작업 수행
# 미들웨어는 모든 요청에 대해 실행되며 , 요청을 처리하기 전에 응답을 반환하기 전에 특정 작업을 수행할 수 있다.
# 예를 들어 , 로깅, 인증 ,cors처리, 압축등

from domain.question import question_router
import logging # 로그 출력용


app = FastAPI(                  # 생성자를 통해서 postman 대체하는 문서화 툴 내장되어 있다.
    title="MBC AI 프로젝트 test",
    description="파이썬과 자바 부트를 연동한 AI 앱",
    version="1.0.0",
    docs_url=None,         #내장된 포스트맨 none 해서 접근 불가하는게 좋다.          포트/docs  보안상 none 처리
    redoc_url=None         # 포트/redoc       보안상 none 처리
)                 # FastAPI() 객체 생성해서 app 변수에 넣음

class LoggingMiddleware(BaseHTTPMiddleware):    # 로그를 콘솔에 출력하는 용도
    logging.basicConfig(level=logging.INFO) # 로그 출력 추가
    async def dispatch(self,request,call_next):
        logging.info(f"Req: {request.method}{request.url}")
        response = await call_next(request)
        logging.info(f"Status Code :{response.status_code}")
        return response
app.add_middleware(LoggingMiddleware)       # 모든 요청에 대해 로그를 남기는 미들웨어 클래스를 사용함

class Item(BaseModel):          # 아이템 객체 생성( BaseModel : 객체 연결 -> 상속)
    name : str                  # 필드1 : 상품명 : 문자열
    description : str = None    # 필드2 : 설명 : 문자열(null)
    price : float               # 핃르3 : 가격 : 실수형
    tax : float = None          # 필드4 : 세금 : 실수형(null)

# 컨트롤러 검증은 postman으로 활용해 보았는데 내장된 백 검증 툴도 있다.

@app.get("/")   # http://ip주소:포트/(루트컨텍스트)
async def read_root():
    return {"Hello ": "world"}


@app.post("/items/")        # post 메서드용 응답
async def create_item(item : Item): #BaseModel 은 데이터 모델링을 쉽게 도와주고 유효성 검사를 수행
    # 잘못된 데이터가 들어오면 422 오류코드를 반환
    return item


@app.get("/items/{item_id}")    # http://ip주소:포트/items/1
async def read_item(item_id : int, q : str = None ):
    return {"item_id" : item_id , "q" : q}
    # item_id : 상품의 번호 -> 경로 매개 변수
    # q : 쿼리 매개 변수( 기본값 None)

app.include_router(question_router.router)
