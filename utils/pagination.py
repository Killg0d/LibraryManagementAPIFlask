from flask import request, jsonify


def paginate(query_results, page, per_page):
    """
    Paginate the query results.

    Args:
        query_results (list): List of items (books or any other data).
        page (int): Current page number.
        per_page (int): Number of items per page.

    Returns:
        dict: Paginated results including metadata.
    """
    total_items = len(query_results)
    total_pages = (total_items + per_page - 1) // per_page  # Calculate total pages
    
    if page > total_pages or page < 1:
        return {
            "error": "Invalid page number",
            "total_pages": total_pages,
            "current_page": page,
            "per_page": per_page,
        }, 400
    
    # Determine start and end indices for slicing
    start = (page - 1) * per_page
    end = start + per_page

    # Slice the query results
    items = query_results[start:end]
    
    return {
        "items": items,
        "total_items": total_items,
        "total_pages": total_pages,
        "current_page": page,
        "per_page": per_page,
    }
