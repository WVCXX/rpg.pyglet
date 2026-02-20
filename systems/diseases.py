import random
from typing import Dict, List, Optional

class DiseaseSystem:
    """Система болезней"""
    def __init__(self):
        self.diseases = {
            "простуда": {
                "name": "Простуда",
                "symptoms": ["кашель", "насморк", "температура", "чихание", "головная боль"],
                "duration": (3, 7),
                "effects": {
                    "здоровье": -5,
                    "выносливость": -10,
                    "сила": -2,
                    "ловкость": -2
                },
                "contagious": True,
                "treatment": ["отдых", "травы", "зелье"],
                "deadly": False,
                "cure_chance": 0.7
            },
            "заражение_раны": {
                "name": "Заражение раны",
                "symptoms": ["лихорадка", "гной", "слабость", "озноб", "краснота"],
                "duration": (5, 14),
                "effects": {
                    "здоровье": -15,
                    "выносливость": -20,
                    "сила": -5,
                    "ловкость": -3
                },
                "contagious": False,
                "treatment": ["хирургия", "сильные_травы", "магия"],
                "deadly": True,
                "cure_chance": 0.5
            },
            "чума": {
                "name": "Чума",
                "symptoms": ["бубоны", "кровотечение", "бред", "черные точки", "высокая температура"],
                "duration": (7, 21),
                "effects": {
                    "здоровье": -30,
                    "выносливость": -40,
                    "сила": -10,
                    "ловкость": -8,
                    "харизма": -15,
                    "удача": -20
                },
                "contagious": True,
                "treatment": ["карантин", "редкие_травы", "мощная_магия"],
                "deadly": True,
                "cure_chance": 0.3
            },
            "кровавый_кашель": {
                "name": "Кровавый кашель",
                "symptoms": ["кашель с кровью", "боль в груди", "бледность", "слабость", "одышка"],
                "duration": (10, 30),
                "effects": {
                    "здоровье": -20,
                    "выносливость": -30,
                    "сила": -8,
                    "ловкость": -5
                },
                "contagious": True,
                "treatment": ["постельный_режим", "специальное_лекарство", "святая_вода"],
                "deadly": True,
                "cure_chance": 0.4
            },
            "безумие": {
                "name": "Безумие",
                "symptoms": ["галлюцинации", "паранойя", "агрессия", "бессонница", "навязчивые мысли"],
                "duration": (30, 100),
                "effects": {
                    "интеллект": -15,
                    "мудрость": -20,
                    "харизма": -25,
                    "удача": -30
                },
                "contagious": False,
                "treatment": ["экзорцизм", "редкие_травы", "ментальная_магия"],
                "deadly": False,
                "cure_chance": 0.2
            },
            "лихорадка": {
                "name": "Тропическая лихорадка",
                "symptoms": ["жар", "потливость", "озноб", "слабость", "ломота"],
                "duration": (5, 10),
                "effects": {
                    "здоровье": -10,
                    "выносливость": -15,
                    "сила": -3,
                    "ловкость": -3
                },
                "contagious": False,
                "treatment": ["хинин", "отдых", "травы"],
                "deadly": True,
                "cure_chance": 0.6
            },
            "проказа": {
                "name": "Проказа",
                "symptoms": ["язвы", "потеря чувствительности", "обезображивание", "слабость"],
                "duration": (60, 180),
                "effects": {
                    "здоровье": -25,
                    "харизма": -40,
                    "сила": -10,
                    "ловкость": -10
                },
                "contagious": True,
                "treatment": ["изоляция", "редкие_масла", "чудо"],
                "deadly": True,
                "cure_chance": 0.1
            },
            "белая_горячка": {
                "name": "Белая горячка",
                "symptoms": ["тряска", "видения", "агрессия", "судороги", "страх"],
                "duration": (3, 10),
                "effects": {
                    "интеллект": -20,
                    "мудрость": -25,
                    "харизма": -30,
                    "ловкость": -15
                },
                "contagious": False,
                "treatment": ["трезвость", "отдых", "лекарь"],
                "deadly": True,
                "cure_chance": 0.5
            }
        }
        
        self.active_diseases = []
        self.herbs = {
            "ромашка": {"cures": ["простуда"], "effect": 40, "common": True},
            "шалфей": {"cures": ["простуда", "лихорадка"], "effect": 50, "common": True},
            "чеснок": {"cures": ["простуда", "заражение_раны"], "effect": 30, "common": True},
            "зверобой": {"cures": ["заражение_раны", "лихорадка"], "effect": 40, "common": True},
            "полынь": {"cures": ["лихорадка", "белая_горячка"], "effect": 35, "common": True},
            "редкая_трава": {"cures": ["чума", "кровавый_кашель"], "effect": 60, "rare": True},
            "корень_мандрагоры": {"cures": ["безумие", "проказа"], "effect": 70, "rare": True},
            "слеза_единорога": {"cures": ["чума", "проказа", "безумие"], "effect": 90, "legendary": True},
            "золотой_корень": {"cures": ["кровавый_кашель", "заражение_раны"], "effect": 65, "rare": True}
        }
        
        self.treatments = {
            "лекарь": {"cost": 50, "effect": 0.5, "description": "Лечение у местного лекаря"},
            "жрец": {"cost": 100, "effect": 0.7, "description": "Молитвы в храме"},
            "маг": {"cost": 200, "effect": 0.9, "description": "Магическое исцеление"},
            "хирург": {"cost": 150, "effect": 0.6, "description": "Хирургическое вмешательство"},
            "травник": {"cost": 30, "effect": 0.4, "description": "Лечение травами"}
        }
    
    def infect(self, disease_id: str, player, source: str = "unknown") -> bool:
        """Заражение болезнью"""
        if disease_id not in self.diseases:
            return False
        
        # проверка на уже существующую болезнь
        for existing in self.active_diseases:
            if existing["id"] == disease_id:
                return False  # уже болен
        
        disease = self.diseases[disease_id].copy()
        
        # шанс заражения зависит от источника
        chance = 1.0
        if source == "creature":
            chance = 0.3
        elif source == "food":
            chance = 0.5
        elif source == "environment":
            chance = 0.2
        elif source == "contagion":
            chance = 0.7
        
        if random.random() > chance:
            return False
        
        # длительность
        duration = random.randint(*disease["duration"])
        
        infection = {
            "id": disease_id,
            "name": disease["name"],
            "symptoms": random.sample(disease["symptoms"], min(3, len(disease["symptoms"]))),
            "days_infected": 0,
            "duration": duration,
            "effects": disease["effects"].copy(),
            "contagious": disease["contagious"],
            "treatment": disease["treatment"],
            "deadly": disease.get("deadly", False),
            "cure_chance": disease.get("cure_chance", 0.5),
            "source": source,
            "stage": 1  # стадия болезни
        }
        
        self.active_diseases.append(infection)
        self.apply_effects(infection, player, add=True)
        
        return True
    
    def apply_effects(self, infection: Dict, player, add: bool = True):
        """Применение эффектов болезни"""
        multiplier = 1 if add else -1
        
        for effect, value in infection["effects"].items():
            if effect in player.stats:
                player.stats[effect] += value * multiplier
            elif effect == "здоровье":
                player.max_health += value * multiplier
                if player.health > player.max_health:
                    player.health = player.max_health
            elif effect == "выносливость":
                player.max_stamina += value * multiplier
            elif effect == "удача":
                if hasattr(player, 'luck'):
                    player.luck += value * multiplier
    
    def daily_update(self, player) -> Optional[str]:
        """Ежедневное обновление болезней"""
        messages = []
        
        for infection in self.active_diseases[:]:
            infection["days_infected"] += 1
            
            # прогрессия болезни
            progress = infection["days_infected"] / infection["duration"]
            
            # смена стадии
            new_stage = min(3, int(progress * 3) + 1)
            if new_stage > infection["stage"]:
                infection["stage"] = new_stage
                messages.append(f"⚠ Болезнь {infection['name']} перешла в {new_stage} стадию!")
                
                # усиление эффектов
                for effect in infection["effects"]:
                    infection["effects"][effect] = int(infection["effects"][effect] * 1.3)
                self.apply_effects(infection, player, add=False)
                self.apply_effects(infection, player, add=True)
            
            # проверка на смерть
            if infection.get("deadly", False):
                death_chance = 0.02 + (progress * 0.1)
                if random.random() < death_chance:
                    player.health = 0
                    return f"💀 Ты умер от {infection['name']}!"
            
            # ухудшение состояния
            if random.random() < 0.1:
                player.health -= 5
                messages.append(f"🤒 Твое состояние ухудшается из-за {infection['name']}")
            
            # выздоровление
            if infection["days_infected"] >= infection["duration"]:
                if random.random() < infection["cure_chance"]:
                    self.cure(infection["id"], player, complete=True)
                    messages.append(f"✨ Ты поборол {infection['name']}!")
                else:
                    # болезнь затягивается
                    infection["duration"] += random.randint(2, 5)
        
        # распространение болезни
        if any(d["contagious"] for d in self.active_diseases):
            if random.random() < 0.2:
                messages.append("🤧 Ты чихаешь. Кажется, ты можешь заразить других...")
        
        return "\n".join(messages) if messages else None
    
    def cure(self, disease_id: str, player, complete: bool = True) -> Optional[str]:
        """Лечение болезни"""
        for i, infection in enumerate(self.active_diseases):
            if infection["id"] == disease_id:
                # снимаем эффекты
                self.apply_effects(infection, player, add=False)
                
                if complete:
                    self.active_diseases.pop(i)
                    return f"💊 Ты вылечился от {infection['name']}!"
                else:
                    # болезнь прошла сама
                    self.active_diseases.pop(i)
                    return f"🌿 {infection['name']} прошла сама собой"
        
        return None
    
    def treat_with_herb(self, herb_id: str, player) -> str:
        """Лечение травой"""
        if herb_id not in self.herbs:
            return "🌿 У тебя нет такой травы"
        
        herb = self.herbs[herb_id]
        cured_any = False
        results = []
        
        for infection in self.active_diseases[:]:
            if infection["id"] in herb["cures"]:
                chance = herb["effect"] / 100
                if random.random() < chance:
                    self.cure(infection["id"], player)
                    results.append(f"✅ {infection['name']} вылечена!")
                    cured_any = True
                else:
                    results.append(f"❌ {herb_id} не помог от {infection['name']}")
        
        if cured_any:
            return "\n".join(results)
        elif not results:
            return "🌿 Эта трава не помогает от твоих болезней"
        else:
            return "\n".join(results)
    
    def seek_treatment(self, treatment_type: str, player) -> Dict:
        """Обращение за лечением"""
        result = {
            "success": False,
            "message": "",
            "cost": 0,
            "cured": []
        }
        
        if treatment_type not in self.treatments:
            result["message"] = "Нет такого лечения"
            return result
        
        treatment = self.treatments[treatment_type]
        cost = treatment["cost"]
        
        if player.money < cost:
            result["message"] = f"Не хватает денег! Нужно {cost} монет"
            return result
        
        player.money -= cost
        result["cost"] = cost
        
        # лечение каждой болезни
        cured_count = 0
        for infection in self.active_diseases[:]:
            if random.random() < treatment["effect"]:
                self.cure(infection["id"], player)
                cured_count += 1
                result["cured"].append(infection["name"])
        
        if cured_count > 0:
            result["success"] = True
            result["message"] = f"Лечение помогло! Вылечено болезней: {cured_count}"
        else:
            result["message"] = "Лечение не помогло..."
        
        return result
    
    def get_symptoms(self) -> str:
        """Получение симптомов"""
        if not self.active_diseases:
            return "Ты здоров"
        
        all_symptoms = []
        for d in self.active_diseases:
            all_symptoms.extend(d["symptoms"])
        
        # убираем дубликаты
        unique_symptoms = list(set(all_symptoms))
        
        return f"🤒 Симптомы: {', '.join(unique_symptoms)}"
    
    def get_disease_status(self) -> List[Dict]:
        """Получение статуса всех болезней"""
        status = []
        for disease in self.active_diseases:
            status.append({
                "name": disease["name"],
                "days": disease["days_infected"],
                "duration": disease["duration"],
                "stage": disease["stage"],
                "symptoms": disease["symptoms"],
                "deadly": disease.get("deadly", False)
            })
        return status