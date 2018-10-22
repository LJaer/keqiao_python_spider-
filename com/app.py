# encoding=utf-8
from com.service.BlogService import BlogService
from com.service.UserService import UserService
from com.service.CategoryService import CategoryService

if __name__ == '__main__':
    # 获取用户空间信息
    # user_service = UserService()
    # user_service.get_urls()

    # 获取分类信息
    # category_service = CategoryService()
    # category_service.get_all_category_type()

    # 获取文章链接
    blog_servie = BlogService()
    blog_servie.get_all_blog()
