from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db  # certifique-se de que 'app' e 'db' estejam definidos no app.py

# Inicializa o Migrate
migrate = Migrate(app, db)

# Cria o gerenciador
manager = Manager(app)

# Adiciona o comando de migração
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
