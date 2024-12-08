def paginate(data, request):
    """Implements basic pagination."""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    start = (page - 1) * per_page
    end = start + per_page
    return {"data": data[start:end], "page": page, "per_page": per_page, "total": len(data)}
