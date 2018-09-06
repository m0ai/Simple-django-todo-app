# 개발 환경 설정

해당하는 레포짓토리의 소스를 클론하여 로컬에 다운로드합니다.
기본적으로 테스트 환경에서 이는 `docker`로 작동하며 개발된 환경의 도커 버젼은 ```18.06.0-ce-mac70``입니다.

```
docker-compose up -d 
```

서버를 실행시키기 위해 다음과 같은 명령어를 입력합니다.

기본적으로 개발 환경은 `local` 설정 파일을 참조합니다. 이를 변경하기 위해선
`docker-compose.yml` 내에 `DJANGO_SETTINGS_MODULE`를 변경해주면 `docker-compsoe up` 진행 시 변경된 경로의 설정 파일을 참조하여 컨테이너가 로드 됩니다.


__warning__

이 프로젝트는 장고의 민간한 데이터는 `(ex, SECRET_KEY)` 별도의 파일로 따로 관리합니다.
`{proejct_path}/todoapp/settgins/secret.py.template`을 참조하여 개인화된 `{proejct_path}/todoapp/settgins/secret.py`를 생성해야합니다.
`secret.py`는 `base.py`내에서 `import`되며 `development.py, local.py ,producation.py `파일들은 `base.py`를 `import`하는 구조로 되어있습니다.


### Local

`local`환경에선 도커를 이용해 웹앱 컨테이너를 생성합니다. 웹앱 컨테이너 내에 redis와 mysql로 데이터베이스가 동작하며 하나에 컨테이너에서 모든 정보들이 저장되어 집니다.


### Development 

`development` 환경에선 도커를 이용하여 웹앱과 데이터베이스를 나누어 실행됩니다.
django와 postgresql로 실행되며 구조는 다음과 같습니다.


```
                            host:5432                  host:8000                host:6379
                          |-----------|              |-----------|            |-----------|
 docker container part    | postgres  |     < - >    |  django   |    < - >   |   redis   |
                          |___________|              |___________|            |___________|

                          |-----------|
               host  os   | app image |
                          |___________|
```


이후 `docker ps`으로 동작 중인 서비스를 확인 할 수 있습니다.


### Production

현재 배포를 위한 설정과 클라우드/IDC가 구축되어지지 않았습니다. 추가될 시 바로 업데이트 진행하겠습니다.





# TODO API Documentation


## Endpoints

* [To Do 목록 가져오기](#to-do-목록-가져오기) : `GET /api/todos`
* [To Do 생성하기](#to-do-생성하기) : `POST /api/todos`
* [To Do 상세보기](#to-do-상세보기) : `GET /api/todos/{id}`
* [To Do 수정하기](#to-do-수정하기) : `PUT,PATCH /api/todos/{id}`
* [To Do 삭제하기](#to-do-삭제하기) : `DELETE /api/todos/{id}`

## Endpoints for real time sync/socket

* [To Do 삭제 이벤트 브로드캐스터](#to-do-삭제-이벤트-브로드캐스터) : `ws|socket /ws/todos` 
* [To Do 생성 및 수정 이벤트 브로드캐스터](#to-do-생성-및-수정-이벤트-브로드캐스터) : `ws|socket /ws/todos`

## Fields Description 

Todo 갯수는 최대 10만개를 초과 할 수 없습니다.

| Field name | Type | Description |
| :------------ | :-----------: | -------------------: | 
| id | int | Todo의 고유 값 | 
| index | int | Todo 의 순서 (0부터 시작) | 
| title | char | Todo 제목, 최대 80글자, null이 될 수 없음 | 
| content | text | Todo 내용 혹은 설명 | 
| is_done | bool | Todo 작업의 완료 여부 | 
| updated_at | datetime | Todo 수정 시, 데이터 변경 시각 | 
| created_at | datetime | Todo 생성 시각 | 

## To Do 목록 가져오기

전체 To Do 목록을 가져오는 기능 입니다.

**URL** : `/api/todos`

**method** : `GET`

### Success Response 
**Status Code** : `200`

```json
[
    {
        "id": 1,
        "index": 0,
        "title": "밥먹기",
        "content": "두번먹기 세번먹기",
        "is_done": false,
        "created_at": "2018-08-03T03:56:51.946793",
        "updated_at": "2018-08-03T03:56:51.946811"
    } ,
   {
        "id": 2,
        "index": 1,
        "title": "간식먹기",
        "content": "에너지바",
        "is_done": True,
        "created_at": "2018-08-03T03:56:51.946793",
        "updated_at": "2018-08-03T03:56:51.946811"
    }
]
```

## To Do 생성하기 

새로운 Todo를 생성하는 기능입니다.

**URL** : `/api/todos`

**Method** : `POST`

**Parameter** : `title` 

**Optional Parameter** : `content`, `is_done`, `index`

**Request Content**

```json
{
	"title": "밥먹기",
	"content": "두번먹기 세번먹기",
	"is_done": false,
	"index" : 2
}
```

### Success Response 

**Status Code** : `201_CREATE`

``` json
[
    {
        "id": 1,
        "index": 0,
        "title": "밥먹기",
        "content": "두번먹기 세번먹기",
        "is_done": false,
        "created_at": "2018-08-03T03:56:51.946793",
        "updated_at": "2018-08-03T03:56:51.946811"
    }
]
```


### Error Responses
**Conditiion** : 만약 십만개 이상의 Todo가 존재하여 Todo를 더 생성 할 수 없을 때 

**Status Code** : `406_NOT_ACCEPTABLE`

**Content Example** : 

```json
{
    "detail":"The maximum number of todo has been exceeded.
              Please remove the other todos"
}
```

---

**Conditiion** : 만약 `title`이 `null`이거나 빈문자열일 경우

**Status Code** : `400_BAD_REQUEST`

**Content Example** : 

```json
{
	"title": ["This field is required."]
}
```


## To Do 상세보기

하나의 `Todo`정보를 상세히 볼 수 있는 기능입니다.

**URL** : `/api/todos/{id}`

**Method** : `GET`

### Success Response 

**Status Code** : `200_OK`

**Content** : 

```json
{
	"id": 1,
        "index": 1,
	"title": "밥먹기",
	"content": "두번먹기 세번먹기",
	"is_done": false,
	"created_at": "2018-08-03T03:56:51.946793",
	"updated_at": "2018-08-03T03:56:51.946811"
} 
```

### Error Response 

**Conditiion** : 만약 `id`가 비정상적이거나 없는 `id` 일 때 

**Status Code** : `404_NOT_FOUND`

**Content Example** : 

```json
{
	"detail":"Not found."	
}
```


## To Do 수정하기

이미 생성된 `Todo`를 수정할 수 있습니다.

**URL** : `/api/todos/{id}`

**Method** : `PUT` | `PATCH`

**Parameter** : `content` | `is_done` | `title` | `index`

**Request Content** : 

```json
{
	"is_done" : True,
}
```
### Success Response 

**Status Code** : `200_OK`

**Content Example** : 

```json
{
	"id": 1,
	"title": "밥먹기",
        "index": 1,
	"content": "두번먹기 세번먹기",
	"is_done": True,
	"created_at": "2018-08-03T03:56:51.946793",
	"updated_at": "2018-08-03T03:56:51.946811"
} 
```

### Error Response 
**Conditiion** : 만약 `id`가 비정상적이거나 없는 `id` 일 때 

**Status Code** : `404_NOT_FOUND`

**Content Example** : 

```json
{
	"detail":"Not found."	
}
```

---

**Conditiion** : `title`이 `null`이거나 빈문자열 일 때

**Status Code** : `400_BAD_REQUEST`

**Content Example** :

```
{
	"title":["This field may not be blank."]
}
```


## To Do 삭제하기 


하나의 `Todo` 를 삭제할 수 있습니다.

**URL** : `/api/todos/{id}`

**Method** : `DELETE`

### Success Response 

**Status Code** : `204_NO_CONTENT`

**Content Example** : `''`

### Error Response 

**Conditiion** : 만약 `id`가 비정상적이거나 없는 `id` 일 때 

**Status Code** : `404_NOT_FOUND`

**Content Example** : 

```json
{
	"detail":"Not found."	
}
```




## To Do 삭제 이벤트 브로드캐스터

`Todo`가 삭제 될때의 삭제된 `Todo` 정보를 브로드캐스트합니다.

**URL** : `/ws/todos/`

**protocal** : `socket/ws`

**type** : `delete`

**Repsonse Example** : 

```json
{
	"id": 1, 
        "index": 1,
	"title": "Todo1", 
	"content": "hello this is Todo 1", 
	"is_done": true, "created_at": "2018-08-06 15:18:47.553666", 
	"updated_at": "2018-08-06 17:13:05.008990", 
	"type": "delete"
}
```

## To Do 생성 및 수정 이벤트 브로드캐스터

`Todo`가 생성 혹은 수정될때 해당 `Todo`의 정보를 `socket/ws`로 브로드캐스트합니다.


**URL** : `/ws/todos/`

**protocal** : `socket/ws`

**type** : `update_or_create`

**Repsonse Example** : 

```json
{
	"id": 2,

        "index": 1,
	"title": "Test 1", 
	"content": "test", 
	"is_done": true, 
	"created_at": "2018-08-06 15:24:42.157683", 
	"updated_at": "2018-08-06 17:36:41.333084", 
	"type": "update_or_create"
}
```


