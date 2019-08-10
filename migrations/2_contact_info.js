var ContactInfo = artifacts.require("./ContactInfo.sol");

const settings = {
    name: "Alec M. Wantoch",
    email: "alec@wantoch.net",
    github: "https://github.com/awantoch",
    bitcoin: "",
    ethereum: ""
};

module.exports = function(deployer, owner) {
    // Setup deployer function to pass data to contract constructor
    deployer.deploy(
        ContactInfo,
        settings.name,
        settings.email,
        settings.github,
        settings.bitcoin,
        settings.ethereum || owner
    );
};
