from django.core.paginator import Paginator


def split_into_pages(request, instances):
    """
    글 조회 시 query params 추출
    - page=<page_num>: 원하는 페이지 번호
    - size=<size_num>: 페이지 당 영화 개수
    - (인자가 없는 경우 1 페이지, 20개 반환)
    """
    # query 받아오기
    params = request.query_params

    # 페이지 번호
    if 'page' in params:
        page_num = int(params.get('page'))
    else:
        page_num = 1    
    
    # 페이지 당 오브젝트 개수
    if 'size' in params:
        size_num = int(params.get('size'))
    else:
        size_num = 20
    
    # 모델 인스턴스들을 받아, 페이지 수만큼 쪼개서 반환
    paginator = Paginator(instances, size_num)    
    page_obj = paginator.get_page(page_num)
    return page_obj.object_list
