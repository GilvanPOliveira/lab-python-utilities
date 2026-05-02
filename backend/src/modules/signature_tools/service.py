import html


def build_link(label: str, url: str) -> str:
    if not url:
        return ""

    safe_label = html.escape(label)
    safe_url = html.escape(url)

    return f'<a href="{safe_url}" style="color:#0891b2;text-decoration:none;">{safe_label}</a>'


def generate_email_signature(
    full_name: str,
    role: str,
    email: str,
    phone: str,
    website: str,
    github: str,
    linkedin: str,
) -> dict:
    safe_name = html.escape(full_name.strip() or "Seu Nome")
    safe_role = html.escape(role.strip())
    safe_email = html.escape(email.strip())
    safe_phone = html.escape(phone.strip())

    links = []

    if website:
        links.append(build_link("Site", website))

    if github:
        links.append(build_link("GitHub", github))

    if linkedin:
        links.append(build_link("LinkedIn", linkedin))

    links_html = " &nbsp;|&nbsp; ".join(links)

    email_html = ""
    phone_html = ""

    if safe_email:
        email_html = f'<div style="font-size:13px;color:#334155;">Email: {safe_email}</div>'

    if safe_phone:
        phone_html = f'<div style="font-size:13px;color:#334155;">Telefone: {safe_phone}</div>'

    html_signature = f"""
<table cellpadding="0" cellspacing="0" style="font-family:Arial,sans-serif;border-left:4px solid #22d3ee;padding-left:12px;">
  <tr>
    <td style="padding-left:12px;">
      <div style="font-size:18px;font-weight:700;color:#0f172a;">{safe_name}</div>
      <div style="font-size:14px;color:#475569;margin-top:2px;">{safe_role}</div>
      <div style="margin-top:8px;">
        {email_html}
        {phone_html}
      </div>
      <div style="margin-top:8px;font-size:13px;">
        {links_html}
      </div>
    </td>
  </tr>
</table>
""".strip()

    plain_lines = [safe_name]

    if safe_role:
        plain_lines.append(safe_role)

    if safe_email:
        plain_lines.append(f"Email: {safe_email}")

    if safe_phone:
        plain_lines.append(f"Telefone: {safe_phone}")

    if website:
        plain_lines.append(f"Site: {website}")

    if github:
        plain_lines.append(f"GitHub: {github}")

    if linkedin:
        plain_lines.append(f"LinkedIn: {linkedin}")

    return {
        "html": html_signature,
        "plain_text": "\n".join(plain_lines),
    }
