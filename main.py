from usecases.rag import RagUseCase
import ollama

def main():
    path = "storage/chromadb"
    model = "nomic-embed-text"
    table_name = "math"
    data_folder = "./data"
    rag = RagUseCase.from_basic(path=path,model=model,table_name=table_name,data_folder=data_folder)
    while True:
        prompt = input("\nВвeдите вопрос:\n")
        system_instruction = (
            "Вы — строгий ИИ-аналитик данных. Ваша единственная задача — отвечать на вопросы пользователя по линейное математике, "
            "используя ТОЛЬКО предоставленный контекст из базы данных. Используйте исключительно символы UTF-8.\n\n"
            "КРИТИЧЕСКИЕ ПРАВИЛА:\n"
            "1. СТРОГАЯ ИЗОЛЯЦИЯ: Отвечайте исключительно на основе предоставленных фактов, формул и определений. "
            "Вам категорически запрещено использовать любые внешние знания, додумывать физический/математический смысл "
            "или привлекать информацию, которой нет в переданном тексте.\n"
            "2. ЗАПРЕТ НА ГАЛЛЮЦИНАЦИИ: Если в предоставленном контексте базы данных нет прямого ответа на вопрос пользователя, "
            "или данных недостаточно — вы обязаны четко и прямо ответить: «В предоставленной базе данных нет информации для ответа на этот вопрос».\n"
            "3. БЕРЕЖНОСТЬ К ДАННЫМ: Не изменяйте математические формулы, свойства и знаки. Соберите их в логичный, "
            "структурированный текст без искажения исходного смысла.\n"
            "4. СТИЛЬ: Ответ должен быть сухим, точным, структурированным (используйте списки и Markdown) и по существу, без вводных фраз и «воды»."
        )

        prompt_for_rag = f"""
            [ROLE]
            Ты — специализированный ИИ-модуль оптимизации поисковых запросов в RAG-системе (Retrieval-Augmented Generation), работающий по методологии HyDE (Hypothetical Document Embeddings).

            [TASK]
            Возьми сырой, нечеткий или короткий вопрос пользователя и преобразуй его в ОДИН плотный абзац текста (гипотетический ответ/документ), который с высокой вероятностью содержится в базе знаний. Используй профессиональную техническую лексику, синонимы, отраслевой сленг и ключевые слова, оптимизированные для векторного поиска (векторных эмбеддингов и косинусного сходства).

            [CONSTRAINTS]
            - Верни ИСКЛЮЧИТЕЛЬНО сгенерированный абзац текста для поиска.
            - КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО: отвечать на вопрос пользователя, использовать вводные фразы (например, "Вот гипотетический текст:", "Идеальный текст для поиска:"), давать пояснения или использовать кавычки вокруг результата.
            - Длина текста: строго до 100 слов.
            - Пиши в утвердительной форме, как готовый фрагмент из технической документации или базы знаний.

            [USER_QUERY]
            "{prompt}"

            [HYPOTHETICAL_DOCUMENT]
            """
        
        
        response_for_rag = ollama.generate(
             model='deepseek-r1:14b', 
             prompt = prompt_for_rag,
             options={
                 'temperature': 0.2,  
             },
            think=False,
         )
        prompt_search = response_for_rag["response"]
        
        responses = rag.advanse_search_by_index(prompt_search)
        db_info = "\n".join(responses['documents'])
        response_final = ollama.chat(
            model="deepseek-r1:14b",
            messages=[
                {'role': 'system', 'content': system_instruction},
                {'role': 'system', 'content': f"Дополнительный контекст: {db_info}"},
                {'role': 'user', 'content': prompt}  
            ],
            stream=True
        )
        for chunk in response_final:
            try:
                think = chunk['message']['thinking']
                if(think):
                    print(think, end="")
            except KeyError:
                break

        for chunk in response_final:
            content = chunk["message"]['content']
            if(content):
                print(content, end="")
            



if __name__ == "__main__":
    main()
    