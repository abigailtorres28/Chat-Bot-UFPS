import asyncio
from agent import chatbot_agent

# Lista de preguntas con sus palabras clave relevantes esperadas
test_cases = [
    ("¿Qué son los exámenes de habilitación?", ["habilitación", "asignatura", "3,0", "2,0"]),
    ("¿Qué es un estudiante condicional?", ["promedio", "condicional", "excluido", "2.8", "3.1"]),
    ("¿Qué promedio mínimo se necesita para aprobar una materia?", ["mínimo", "aprobar", "materia", "3,0"]),
    ("¿Cuáles son los requisitos para que un egresado curse otra carrera en la UFPS?", ["egresado", "requisitos", "título", "3,5", "solicitud", "consejo"]),
    ("¿Qué se entiende por estudiante regular?", ["estudiante", "regular", "matrícula", "plan de estudios"]),
    ("¿Qué requisitos deben cumplir los estudiantes nuevos para su matrícula?", ["certificado", "salud", "documento", "pago", "matrícula"]),
    ("¿Qué sucede si un estudiante pierde más de tres materias en el primer semestre?", ["pierde", "tres", "materias", "excluido"]),
    ("¿Qué se requiere para ser admitido como estudiante especial?", ["estudiante", "especial", "extensión", "consejo académico"]),
    ("¿Cuántas veces puede un estudiante solicitar reserva de cupo?", ["reserva", "cupo", "dos", "facultad"]),
    ("¿Qué beneficios tienen los estudiantes víctimas del conflicto armado?", ["víctimas", "conflicto", "exención", "promedio", "beca-trabajo"]),
    ("¿Cuándo inician las clases?", ["5", "febrero", "2025"]),
    ("¿Cuál es la fecha límite para pagar matrícula extraordinaria (segunda fecha)?", ["3", "febrero", "2025"]),
    ("¿Cuándo se realiza la inducción a padres y estudiantes?", ["inducción", "29", "30", "31", "enero", "2025"]),
    ("¿Cuándo es la fecha límite para la cancelación ordinaria parcial o total de materias?", ["21", "marzo"]),
    ("¿Cuándo se puede iniciar la postulación a beca-trabajo y monitoría?", ["17", "21", "febrero", "2025"]),
    ("¿En qué fechas se realizan los primeros exámenes previos?", ["25", "marzo", "7", "abril"]),
    ("¿Cuándo finalizan las clases?", ["31", "mayo", "2025"]),
    ("¿Qué días se presentan los exámenes finales?", ["3", "13", "junio", "2025"]),
    ("¿Cuándo se realizan los exámenes de habilitación y validación?", ["16", "18", "junio"]),
    ("¿En qué fecha inicia el receso académico?", ["24", "junio", "2025"]),
]

def evaluar_respuesta(respuesta, keywords):
    if any(k.isdigit() and len(k) == 4 for k in keywords):  # hay año (ej: 2025)
        # Si hay una fecha en los keywords, que al menos la parte principal esté
        return any(k in respuesta for k in keywords if k.isdigit() or k in ["enero", "febrero", "marzo", "abril", "mayo", "junio"])
    else:
        # Si no es fecha, bastará con al menos 2 palabras clave presentes
        coincidencias = [k for k in keywords if k.lower() in respuesta.lower()]
        return len(coincidencias) >= 2


# Función principal
async def run_tests():
    print("🔍 Iniciando evaluación del chatbot...\n")
    aciertos = 0
    for i, (pregunta, keywords) in enumerate(test_cases, start=1):
        print(f"🧪 Pregunta {i}: {pregunta}")
        respuesta = await chatbot_agent(pregunta)
        print(f"🤖 Respuesta: {respuesta}")
        if evaluar_respuesta(respuesta, keywords):
            print("✅ Relevancia detectada\n")
            aciertos += 1
        else:
            print(f"❌ Faltan palabras clave: {[kw for kw in keywords if kw.lower() not in respuesta.lower()]}\n")
    total = len(test_cases)
    print(f"📊 Resultado final: {aciertos}/{total} respuestas relevantes ({(aciertos/total)*100:.1f}%)")

# Ejecutar
if __name__ == "__main__":
    asyncio.run(run_tests())
