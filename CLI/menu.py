import click
from CLI import banner, plugin_manager

@click.command()
def menu():
    pm = plugin_manager.PluginManager()
    pm.load_plugins()

    banner.print_wave_banner()

    while True:
        click.echo("\n1. List Plugins")
        click.echo("2. Run Plugin")
        click.echo("0. Exit")

        choice = click.prompt("Enter your choice", type=int)

        if choice == 0:
            # exit the program
            click.echo("Goodbye!")
            return "exit"
        elif choice == 1:
            # List available plugins
            click.echo("\nAvailable Plugins:")
            if not pm.plugins:
                click.echo("No plugins found.")
            else:
                pm.list_plugins()
        elif choice == 2:
            if not pm.plugins:
                click.echo("\nNo plugins to run. Please add plugins to the directory.")
                continue

            click.echo("\nAvailable Plugins:")
            pm.list_plugins()

            plugin_choice = click.prompt("Select a plugin by number", type=int)
            if plugin_choice < 1 or plugin_choice > len(pm.plugins):
                click.echo("Invalid plugin number.")
                continue

            selected_plugin = pm.plugins[plugin_choice - 1]
            click.echo(f"Selected Plugin: {selected_plugin.get_name()}")
            return "plugin", selected_plugin
        else:
            click.echo("Invalid choice.")


if __name__ == "__main__":
    menu()


