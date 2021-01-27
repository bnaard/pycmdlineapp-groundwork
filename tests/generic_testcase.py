
import pytest

class GenericTestCase:    

    @pytest.fixture(autouse=True, scope="session")
    def config_logging(self):
        pass
        # config_instance = dingest.common.config.DingestConfig()
        # config_instance.load_base_config()
        # logging.config.dictConfig(config_instance.config["logging"])
        # log = logging.getLogger("dingest")
        # echo = logging.getLogger("dingest.echo")
        
        # # running tests is clearly debug mode so overwrite whatever logging setting is in default
        # log.setLevel(logging.DEBUG)
        # echo.setLevel(logging.DEBUG)