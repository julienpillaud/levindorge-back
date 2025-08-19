from cleanstack.domain import BaseDomain, CommandHandler

from app.domain.articles.commands import (
    create_article_command,
    delete_article_command,
    get_article_command,
    get_articles_command,
    update_article_command,
)
from app.domain.context import ContextProtocol


class Domain(BaseDomain[ContextProtocol]):
    get_articles = CommandHandler(get_articles_command)
    get_article = CommandHandler(get_article_command)
    create_article = CommandHandler(create_article_command)
    update_article = CommandHandler(update_article_command)
    delete_article = CommandHandler(delete_article_command)
