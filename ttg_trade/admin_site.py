"""
T&TG Trade Corp — Custom Admin Site
Branded Django admin dashboard.
"""
from django.contrib.admin import AdminSite
from django.utils.html import format_html


class TTGAdminSite(AdminSite):
    site_header  = format_html(
        '<span style="font-family:serif; font-size:1.3rem; font-weight:700; color:#c9a84c;">'
        'T&TG Trade Corp</span>'
        '<span style="font-size:0.8rem; color:#8a9ab5; margin-left:0.5rem;">Admin Panel</span>'
    )
    site_title   = 'T&TG Trade Corp Admin'
    index_title  = 'Administration Dashboard'
    site_url     = '/'


ttg_admin = TTGAdminSite(name='ttg_admin')
