#!/usr/bin/env python3
"""
Exemple d'utilisation du service FAQ Finance Chatbot
Démontre comment utiliser l'API REST pour poser des questions
"""

import requests
import time
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8001"
CHAT_ENDPOINT = f"{BASE_URL}/chat"

def ask_question(question: str) -> Dict[str, Any]:
    """
    Pose une question au chatbot FAQ Finance

    Args:
        question (str): La question à poser

    Returns:
        dict: Réponse du chatbot avec 'answer' et 'sources'
    """
    try:
        response = requests.post(
            CHAT_ENDPOINT,
            json={"message": question},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        print("❌ Erreur : Impossible de se connecter au service.")
        print("   Assurez-vous que le service est démarré sur http://localhost:8001")
        return {"error": "Connection failed"}
    except requests.exceptions.HTTPError as e:
        print(f"❌ Erreur HTTP: {e}")
        return {"error": str(e)}

def check_service_health() -> bool:
    """Vérifie si le service est disponible"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        return response.status_code == 200
    except:
        return False

def demo_questions():
    """Démontre l'utilisation avec différentes questions"""

    print("Démonstration du chatbot FAQ Finance")
    print("=" * 60)

    # Vérification de la santé du service
    if not check_service_health():
        print("Le service n'est pas disponible.")
        print("   Démarrez-le avec: python main.py")
        return

    print("Service connecté et fonctionnel!")
    print()

    # Questions de démonstration
    demo_questions_list = [
        # Questions exactes de la FAQ
        "Qu'est-ce que l'EBITDA ?",
        "Comment calculer le ROE ?",
        "C'est quoi le Free Cash Flow ?",

        # Questions avec variations
        "Peux-tu m'expliquer la marge brute ?",
        "Dette nette définition",
        "CAPEX investissement",

        # Questions avec mots-clés
        "liquidité ratio",
        "working capital",
        "point mort breakeven",

        # Question hors sujet
        "Comment faire une tarte aux pommes ?"
    ]

    for i, question in enumerate(demo_questions_list, 1):
        print(f"Question {i}/10:")
        print(f"   '{question}'")
        print()

        # Poser la question
        result = ask_question(question)

        if "error" in result:
            print("Erreur lors de la requête")
            continue

        # Afficher la réponse
        print("Réponse:")
        print(f"   {result.get('answer', 'Pas de réponse')}")
        print()

        # Afficher les sources
        sources = result.get('sources', [])
        if sources:
            print(f"Sources: {', '.join(sources)}")
        else:
            print("Sources: Aucune (réponse par défaut)")

        print("-" * 60)
        time.sleep(0.5)  # Petite pause pour la lisibilité

def interactive_mode():
    """Mode interactif pour poser ses propres questions"""

    print("\nMode interactif - Posez vos questions sur la finance!")
    print("(Tapez 'quit' ou 'exit' pour quitter)")
    print("=" * 60)

    if not check_service_health():
        print("Le service n'est pas disponible.")
        return

    while True:
        try:
            question = input("\nVotre question: ").strip()

            if question.lower() in ['quit', 'exit', 'q']:
                print("Au revoir!")
                break

            if not question:
                print("Veuillez poser une question.")
                continue

            result = ask_question(question)

            if "error" in result:
                print("Erreur lors de la requête")
                continue

            print("\nRéponse:")
            print(f"   {result.get('answer', 'Pas de réponse')}")

            sources = result.get('sources', [])
            if sources:
                print(f"\nSources: {', '.join(sources)}")

        except KeyboardInterrupt:
            print("\n\nAu revoir!")
            break
        except Exception as e:
            print(f"Erreur inattendue: {e}")

def benchmark_performance():
    """Test de performance avec plusieurs requêtes"""

    print("\nTest de performance")
    print("=" * 60)

    if not check_service_health():
        print("Le service n'est pas disponible.")
        return

    test_questions = [
        "EBITDA",
        "marge brute",
        "cash flow",
        "ROE calcul",
        "dette nette"
    ]

    print(f"Test avec {len(test_questions)} questions...")

    start_time = time.time()
    successful_requests = 0

    for question in test_questions:
        result = ask_question(question)
        if "error" not in result:
            successful_requests += 1

    end_time = time.time()
    total_time = end_time - start_time

    print(f"{successful_requests}/{len(test_questions)} requêtes réussies")
    print(f"Temps total: {total_time:.2f}s")
    print(f"Moyenne: {total_time/len(test_questions):.3f}s par requête")

def main():
    """Fonction principale avec menu de choix"""

    print("FAQ Finance Chatbot - Exemple d'utilisation")
    print("=" * 60)
    print("Choisissez une option:")
    print("1. Démonstration avec questions prédéfinies")
    print("2. Mode interactif")
    print("3. Test de performance")
    print("4. Vérifier la santé du service")
    print("5. Quitter")

    while True:
        try:
            choice = input("\nVotre choix (1-5): ").strip()

            if choice == "1":
                demo_questions()
            elif choice == "2":
                interactive_mode()
            elif choice == "3":
                benchmark_performance()
            elif choice == "4":
                if check_service_health():
                    print("Service disponible et fonctionnel!")
                else:
                    print("Service non disponible.")
                    print("   Démarrez-le avec: python main.py")
            elif choice == "5":
                print("Au revoir!")
                break
            else:
                print("Choix invalide. Veuillez choisir entre 1 et 5.")

        except KeyboardInterrupt:
            print("\n\nAu revoir!")
            break
        except Exception as e:
            print(f"Erreur inattendue: {e}")

if __name__ == "__main__":
    main()
