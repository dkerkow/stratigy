Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty32"
  config.vm.synced_folder ".", "/vagrant"
  config.vm.network :forwarded_port, host: 5000, guest: 5000
  config.vm.network :forwarded_port, host: 5433, guest: 5432
  config.vm.provider :virtualbox do |v|
    v.customize ["modifyvm", :id, "--cpuexecutioncap", "50"]
    v.memory = 512
  end
  config.vm.provision "shell", path: "provisioning/provision.sh"
end
