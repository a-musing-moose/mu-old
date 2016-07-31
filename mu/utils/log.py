import logging
import logging.config

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(levelname)s] %(message)s (%(name)s)',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'mu': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}


def initialise_logging(settings):
    new_config = DEFAULT_LOGGING.copy()
    if hasattr(settings, 'logging'):
        new_config.update(settings.logging)
    logging.config.dictConfig(new_config)
