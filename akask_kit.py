import os
import sys
import tempfile 
import shutil
import subprocess

class akash_kit:
    def __init__(self, resources, meta=None):
        if meta is None:
            meta = {}
            if os.geteuid() == 0:
                self.akash_path = "/usr/local/bin/"
            else:
                self.akash_path = os.path.expanduser("~/.akash/bin/")
                pass
        else:
            if "akash_path" in meta:
                self.akash_path = meta["akash_path"]
            else:
                if os.geteuid() == 0:
                    self.akash_path = "/usr/local/bin/"
                else:
                    self.akash_path = os.path.expanduser("~/.akash/bin/")
                    pass
        if not os.path.exists(self.akash_path):
            os.makedirs(self.akash_path)
        os.environ['PATH'] = os.environ['PATH'] + ":" + self.akash_path

    def install_akash_cli(self, **kwargs):
        akash_path = ""
        which_unzip = os.system("which unzip")
        if which_unzip != 0:
            os.system("sudo apt-get install unzip")
        which_jq = os.system("which jq")
        if which_jq != 0:
            os.system("sudo apt-get install jq")

        if "akash_path" in kwargs:
            akash_path = kwargs["akash_path"]
        elif self.akash_path is not None:
            akash_path = self.akash_path
        else:
            if os.geteuid() == 0:
                akash_path = "/usr/local/bin/"
            else:
                akash_path = os.path.expanduser("~/.akash/bin/")
                pass

        os.system("cd /tmp && curl -sfL https://raw.githubusercontent.com/akash-network/provider/main/install.sh | bash")
        os.system("mv /tmp/bin/provider-services " + akash_path)

        if os.geteuid() != 0:
            os.system('echo \'export PATH="$HOME/.akash/bin:$PATH"\' >> ~/.bashrc')
        
        return self.test_install_akash_cli()

    def test_install_akash_cli(self, **kwargs):
        env = os.environ.copy()
        env['PATH'] = env['PATH'] + ":" + self.akash_path
        try:
            test = subprocess.check_output('which provider-services', shell=True, env=env).decode('utf-8').replace("\n", "")
            version = subprocess.check_output('provider-services version', shell=True, env=env).decode('utf-8')
        except subprocess.CalledProcessError as e:
            return False
        finally:
            return True

if __name__ == "__main__":
    akash = akash_kit({})
    results = akash.install_akash_cli()
    if results:
        print("Akash CLI installed successfully")
    else:
        print("Akash CLI installation failed")
    pass