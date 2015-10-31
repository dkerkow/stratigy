Vagrant.configure("2") do |config|

  config.vm.box = "fgrehm/trusty64-lxc"

  config.vm.synced_folder ".", "/vagrant"

  config.vm.network :forwarded_port, host: 5000, guest: 5000
  config.vm.network :forwarded_port, host: 5433, guest: 5432

  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--cpuexecutioncap", "50"]
    vb.memory = 300
  end

  config.vm.provider :lxc do |lxc|
    lxc.customize 'cgroup.memory.limit_in_bytes', '300M'
  end

  config.vm.provision "shell", path: "provisioning/provision.sh"
end
