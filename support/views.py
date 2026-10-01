from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import KnowledgeArticle
from .ai_service import generate_ai_answer

def home_view(request):
    """
    Renders the Home Page with search box, category pills, and recent articles.
    """
    recent_articles = KnowledgeArticle.objects.all()[:6]
    total_articles = KnowledgeArticle.objects.count()
    
    categories = [
        {'name': 'Network & Wi-Fi', 'icon': 'wifi', 'count': KnowledgeArticle.objects.filter(category='Network & Wi-Fi').count()},
        {'name': 'Operating System', 'icon': 'desktop', 'count': KnowledgeArticle.objects.filter(category='Operating System').count()},
        {'name': 'Software & Hardware', 'icon': 'cpu', 'count': KnowledgeArticle.objects.filter(category='Software & Hardware').count()},
        {'name': 'Account & Security', 'icon': 'shield', 'count': KnowledgeArticle.objects.filter(category='Account & Security').count()},
        {'name': 'Programming & Development', 'icon': 'code', 'count': KnowledgeArticle.objects.filter(category='Programming & Development').count()},
        {'name': 'General IT Support', 'icon': 'help-circle', 'count': KnowledgeArticle.objects.filter(category='General IT Support').count()},
    ]

    context = {
        'recent_articles': recent_articles,
        'total_articles': total_articles,
        'categories': categories,
    }
    return render(request, 'support/home.html', context)


def answer_view(request):
    """
    Processes user query, searches SQLite database for matching articles,
    sends context to Gemini API, and renders the Answer Page.
    """
    query = request.GET.get('q', '').strip() or request.POST.get('question', '').strip()
    
    if not query:
        return redirect('home')

    # Keyword search algorithm across multiple fields using Q objects
    search_words = [w for w in query.split() if len(w) > 2]
    
    q_objects = Q()
    # Exact phrase or broad matches first
    q_objects |= Q(title__icontains=query)
    q_objects |= Q(keywords__icontains=query)
    q_objects |= Q(category__icontains=query)
    q_objects |= Q(problem__icontains=query)
    
    # Also search individual keywords
    for word in search_words:
        q_objects |= Q(title__icontains=word)
        q_objects |= Q(keywords__icontains=word)
        q_objects |= Q(problem__icontains=word)
        q_objects |= Q(solution__icontains=word)

    matching_articles = KnowledgeArticle.objects.filter(q_objects).distinct()[:5]

    # Determine primary category matched
    if matching_articles.exists():
        primary_category = matching_articles.first().category
    else:
        primary_category = 'General Support'

    # Send relevant info to Gemini AI
    ai_response = generate_ai_answer(query, list(matching_articles))

    context = {
        'user_question': query,
        'primary_category': primary_category,
        'ai_result': ai_response,
        'related_articles': matching_articles,
        'article_count': matching_articles.count(),
    }
    return render(request, 'support/answer.html', context)


def article_list_view(request):
    """
    Renders list of all knowledge base articles with search & category filtering.
    """
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    articles = KnowledgeArticle.objects.all()

    if category:
        articles = articles.filter(category=category)

    if query:
        articles = articles.filter(
            Q(title__icontains=query) |
            Q(keywords__icontains=query) |
            Q(problem__icontains=query) |
            Q(solution__icontains=query)
        ).distinct()

    categories = [c[0] for c in KnowledgeArticle.CATEGORY_CHOICES]

    context = {
        'articles': articles,
        'selected_category': category,
        'search_query': query,
        'categories': categories,
        'total_count': articles.count(),
    }
    return render(request, 'support/articles_list.html', context)


def article_detail_view(request, pk):
    """
    Displays individual Knowledge Article details.
    """
    article = get_object_or_404(KnowledgeArticle, pk=pk)
    related_articles = KnowledgeArticle.objects.filter(
        category=article.category
    ).exclude(pk=article.pk)[:4]

    context = {
        'article': article,
        'related_articles': related_articles,
    }
    return render(request, 'support/article_detail.html', context)
