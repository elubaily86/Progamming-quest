window.TESTFLOW_DATA = {
  tests: [
    {id:'ent-math', title:'ЕНТ: математика', category:'school', level:'Средний', questions:35, time:60, score:78, icon:'calc', desc:'Алгебра, функции, проценты и логика для подготовки к экзамену.'},
    {id:'python-junior', title:'Python Junior', category:'it', level:'Лёгкий', questions:28, time:45, score:84, icon:'code', desc:'Типы данных, функции, списки, словари и базовый ООП.'},
    {id:'cyber-basic', title:'Кибербезопасность', category:'security', level:'Сложный', questions:40, time:50, score:71, icon:'shield', desc:'Фишинг, пароли, 2FA, социальная инженерия и безопасное поведение.'},
    {id:'hr-soft', title:'HR Soft Skills', category:'hr', level:'Средний', questions:24, time:30, score:88, icon:'people', desc:'Коммуникация, конфликтология, ответственность и командная работа.'},
    {id:'frontend', title:'Frontend основы', category:'it', level:'Средний', questions:32, time:45, score:80, icon:'layout', desc:'HTML, CSS, доступность, DOM и базовые паттерны интерфейса.'},
    {id:'history', title:'История Казахстана', category:'school', level:'Средний', questions:30, time:40, score:76, icon:'book', desc:'Ключевые даты, личности, события и причинно-следственные связи.'},
    {id:'work-safety', title:'Охрана труда', category:'security', level:'Лёгкий', questions:22, time:25, score:91, icon:'helmet', desc:'Инструктаж, риски, средства защиты и правила рабочего места.'},
    {id:'manager', title:'Менеджмент', category:'hr', level:'Сложный', questions:36, time:50, score:69, icon:'chart', desc:'Планирование, KPI, мотивация, делегирование и контроль результата.'}
  ],
  demoQuestions: [
    {q:'Что делает localStorage?', a:['Хранит данные в браузере между сессиями','Очищает DOM после перезагрузки','Запускает серверный код','Сжимает изображения'], correct:0},
    {q:'Что важно для доступности теста?', a:['Только яркие цвета','Tab-навигация и aria-метки','Запрет клавиатуры','Скрытый текст'], correct:1},
    {q:'Зачем нужен passing score?', a:['Для порога успешного прохождения','Для смены темы','Для drag & drop','Для lazy loading'], correct:0},
    {q:'Что улучшает производительность интерфейса?', a:['Частые reflow','Transform-анимации','Большие несжатые фото','Синхронные блокировки'], correct:1}
  ],
  builder: [
    {id:'intro', title:'Стартовый экран', desc:'Инструкция, правила и согласие участника'},
    {id:'pool', title:'Банк вопросов', desc:'Категории, сложность, случайная выборка'},
    {id:'timer', title:'Таймер и лимиты', desc:'Время прохождения, предупреждения, автосдача'},
    {id:'review', title:'Проверка ответов', desc:'Баллы, критерии, ручная проверка открытых вопросов'},
    {id:'report', title:'Отчёт', desc:'Процент, ошибки, рекомендации и экспорт'}
  ]
};
