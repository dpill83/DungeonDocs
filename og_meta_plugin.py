"""MkDocs plugin that injects Open Graph and Twitter Card meta tags for link previews."""

from __future__ import annotations

import html
from typing import Any

import mkdocs.plugins


def _escape(s: str) -> str:
    return html.escape(s, quote=True)


def _build_meta_tags(config: mkdocs.plugins.Config, page: Any) -> str:
    """Build og: and twitter: meta tags for the current page."""
    site_url = (config.site_url or "").rstrip("/")
    if not site_url:
        return ""

    title = page.title or config.site_name or ""
    description = ""
    if hasattr(page, "meta") and page.meta:
        description = page.meta.get("description", "") or ""
    if not description:
        description = config.site_description or ""

    image_url = f"{site_url}/images/DungeonDocs-logo.png"
    page_url = f"{site_url}/{page.url}" if page.url else site_url

    lines = [
        f'<meta property="og:type" content="website">',
        f'<meta property="og:title" content="{_escape(title)}">',
        f'<meta property="og:description" content="{_escape(description)}">',
        f'<meta property="og:image" content="{_escape(image_url)}">',
        f'<meta property="og:image:width" content="512">',
        f'<meta property="og:image:height" content="512">',
        f'<meta property="og:image:alt" content="{_escape(config.site_name or "DungeonDocs")} logo">',
        f'<meta property="og:image:type" content="image/png">',
        f'<meta property="og:url" content="{_escape(page_url)}">',
        f'<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{_escape(title)}">',
        f'<meta name="twitter:description" content="{_escape(description)}">',
        f'<meta name="twitter:image" content="{_escape(image_url)}">',
    ]
    return "\n    ".join(lines)


class OgMetaPlugin(mkdocs.plugins.BasePlugin):
    """Inject Open Graph and Twitter Card meta tags so link previews show the logo."""

    def on_post_page(
        self, output: str, page: Any, config: mkdocs.plugins.Config
    ) -> str:
        meta = _build_meta_tags(config, page)
        if not meta:
            return output
        injection = f"\n    {meta}\n  "
        return output.replace("</head>", injection + "</head>", 1)
