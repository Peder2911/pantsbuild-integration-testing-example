python_source(name = "application", source = "application.py")
python_source(name = "integration_testing_utilities", source = "integration_testing_utilities.py")
pex_binary(
   name = "bin",
   entry_point = "application",
   execution_mode = "venv",
   include_tools = True,
   restartable = True,
)
docker_image(
   name = "image",
   repository = "application",
   registries = [
      "local",
   ],
   dependencies = [
      ":bin",
   ],
   instructions = [
      "FROM python:3.9",
      "COPY src/bin.pex /bin.pex",
      "ENTRYPOINT /bin.pex"
   ],
)
python_test(
   name = "integration_test", 
   source = "integration_test.py",
   runtime_package_dependencies = [
      ":image"
   ],
   environment = "__local__"
)
