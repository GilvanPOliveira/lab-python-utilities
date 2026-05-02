from fastapi import HTTPException


def normalize(value: str) -> str:
    return value.strip()


def build_intro(recipient_name: str) -> str:
    name = normalize(recipient_name)

    if name:
        return f"Olá, {name}."

    return "Olá."


def get_tone_sentence(tone: str) -> str:
    normalized = normalize(tone).lower()

    tones = {
        "profissional": "Mantive uma abordagem profissional, clara e objetiva.",
        "amigavel": "Mantive uma abordagem amigável, leve e direta.",
        "direto": "Mantive uma abordagem direta, curta e prática.",
        "formal": "Mantive uma abordagem formal e respeitosa.",
    }

    return tones.get(normalized, tones["profissional"])


def generate_recruiter_message(recipient_name: str, context: str, objective: str, tone: str) -> dict:
    intro = build_intro(recipient_name)
    context_text = normalize(context) or "Vi uma oportunidade que combina com minha experiência e meus projetos."
    objective_text = normalize(objective) or "Gostaria de me colocar à disposição para conversar sobre a vaga."

    message = (
        f"{intro}\n\n"
        f"{context_text}\n\n"
        f"{objective_text}\n\n"
        "Fico à disposição para compartilhar mais detalhes sobre minha experiência e meus projetos.\n\n"
        "Obrigado."
    )

    return {
        "title": "Mensagem para recrutador",
        "message": message,
    }


def generate_follow_up(recipient_name: str, context: str, objective: str, tone: str) -> dict:
    intro = build_intro(recipient_name)
    context_text = normalize(context) or "Estou passando para acompanhar o andamento da nossa conversa."
    objective_text = normalize(objective) or "Gostaria de saber se há alguma atualização ou próximo passo."

    message = (
        f"{intro}\n\n"
        f"{context_text}\n\n"
        f"{objective_text}\n\n"
        "Permaneço à disposição.\n\n"
        "Obrigado."
    )

    return {
        "title": "Follow-up",
        "message": message,
    }


def generate_thank_you(recipient_name: str, context: str, objective: str, tone: str) -> dict:
    intro = build_intro(recipient_name)
    context_text = normalize(context) or "Agradeço pelo contato e pela oportunidade de conversar."
    objective_text = normalize(objective) or "Foi muito bom conhecer melhor a oportunidade e compartilhar um pouco da minha trajetória."

    message = (
        f"{intro}\n\n"
        f"{context_text}\n\n"
        f"{objective_text}\n\n"
        "Fico à disposição para os próximos passos.\n\n"
        "Obrigado."
    )

    return {
        "title": "Agradecimento",
        "message": message,
    }


def generate_linkedin_message(recipient_name: str, context: str, objective: str, tone: str) -> dict:
    intro = build_intro(recipient_name)
    context_text = normalize(context) or "Vi seu perfil/publicação e achei interessante fazer conexão."
    objective_text = normalize(objective) or "Gostaria de acompanhar seus conteúdos e trocar experiências profissionais."

    message = (
        f"{intro}\n\n"
        f"{context_text}\n\n"
        f"{objective_text}"
    )

    return {
        "title": "Mensagem para LinkedIn",
        "message": message,
    }


def generate_short_reply(recipient_name: str, context: str, objective: str, tone: str) -> dict:
    intro = build_intro(recipient_name)
    context_text = normalize(context) or "Obrigado pelo retorno."
    objective_text = normalize(objective) or "Fico à disposição."

    message = (
        f"{intro}\n\n"
        f"{context_text}\n\n"
        f"{objective_text}"
    )

    return {
        "title": "Resposta curta",
        "message": message,
    }


def generate_quick_message(
    message_type: str,
    tone: str,
    recipient_name: str,
    context: str,
    objective: str,
) -> dict:
    normalized_type = normalize(message_type).lower()

    generators = {
        "recruiter": generate_recruiter_message,
        "follow_up": generate_follow_up,
        "thank_you": generate_thank_you,
        "linkedin": generate_linkedin_message,
        "short_reply": generate_short_reply,
    }

    generator = generators.get(normalized_type)

    if not generator:
        raise HTTPException(status_code=400, detail="Tipo de mensagem inválido.")

    result = generator(recipient_name, context, objective, tone)
    result["message"] = f"{result['message']}\n\n---\n{get_tone_sentence(tone)}"

    return result
