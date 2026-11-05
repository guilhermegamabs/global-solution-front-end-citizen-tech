class ApiFailure(Exception):
    codigoStatus = 500
    mensagemUsuario = "Algo deu errado. Tente novamente em instantes."


class ProviderUnavailableError(ApiFailure):
    codigoStatus = 503
    mensagemUsuario = "O serviço de análise está indisponível no momento. Tente novamente em alguns minutos."


class ProviderTimeoutError(ApiFailure):
    codigoStatus = 504
    mensagemUsuario = "A análise demorou mais do que o esperado. Tente novamente em instantes."


class InvalidModelResponseError(ApiFailure):
    codigoStatus = 502
    mensagemUsuario = "Não conseguimos montar a orientação desta vez. Tente novamente."


class RecordNotFoundError(ApiFailure):
    codigoStatus = 404
    mensagemUsuario = "Não encontramos essa solicitação. Faça uma nova análise."


class CepNotFoundError(ApiFailure):
    codigoStatus = 404
    mensagemUsuario = "Não encontramos esse CEP. Confira os números e tente de novo."


class LocationUnavailableError(ApiFailure):
    codigoStatus = 503
    mensagemUsuario = "Não conseguimos localizar esse endereço agora. Tente novamente em instantes."


class UnitsUnavailableError(ApiFailure):
    codigoStatus = 503
    mensagemUsuario = "A lista de UPAs está indisponível no momento. Tente novamente em alguns minutos."


class NoUnitsFoundError(ApiFailure):
    codigoStatus = 404
    mensagemUsuario = "Não encontramos UPAs cadastradas na sua cidade. Procure a unidade de saúde mais próxima."


class InvalidReviewError(ApiFailure):
    codigoStatus = 422
    mensagemUsuario = "Para corrigir a urgência, escolha qual nível você considera correto."
