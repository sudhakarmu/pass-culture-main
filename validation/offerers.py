from models import ApiErrors
from models.api_errors import ConflictError


def check_valid_edition(data):
    invalid_fields_for_patch = set(data.keys()).difference({'iban', 'bic', 'isActive'})
    if invalid_fields_for_patch:
        api_errors = ApiErrors()
        for key in invalid_fields_for_patch:
            api_errors.addError(key, 'Vous ne pouvez pas modifier ce champ')
        raise api_errors


def parse_boolean_param_validated(request):
    validated = request.args.get('validated')
    only_validated_offerers = True

    if validated:
        if validated.lower() in ('true', 'false'):
            only_validated_offerers = validated.lower() == 'true'
        else:
            errors = ApiErrors()
            errors.addError('validated', 'Le paramètre \'validated\' doit être \'true\' ou \'false\'')
            raise errors

    return only_validated_offerers


def check_offerer_is_validated(offerer):
    if offerer.validationToken:
        error = ConflictError()
        error.addError('offerer',
                       'Vous ne pouvez pas créer un deuxième compte pour une structure non validée par la pass Culture')
        raise error
