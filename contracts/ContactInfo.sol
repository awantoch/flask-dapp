pragma solidity ^0.5.0;

// A simple Contact Info Smart Contract
contract ContactInfo {
    address owner;
    string public name;
    string public email;
    string public github;
    string public bitcoin;
    string public ethereum;

    constructor(
        string memory _name,
        string memory _email,
        string memory _github,
        string memory _bitcoin,
        string memory _ethereum
    ) public {
        owner = msg.sender;
        name = _name;
        email = _email;
        github = _github;
        bitcoin = _bitcoin;
        ethereum = _ethereum;
    }

    // use this to restrict functions to specific users
    // like the contract owner (you)
    modifier onlyBy(address _account) {
        require(msg.sender == _account, "Not authorized!");
        _; // original function
    }

    // use this to transfer ownership to a new address
    // if you created a new key/wallet
    function setOwner(address newOwner) public onlyBy(owner) {
        owner = newOwner;
    }

    function setName(string memory newName) public onlyBy(owner) {
        name = newName;
    }

    function setEmail(string memory newEmail) public onlyBy(owner) {
        email = newEmail;
    }

    function setGithub(string memory newGithub) public onlyBy(owner) {
        github = newGithub;
    }

    function setBitcoin(string memory newAddress) public onlyBy(owner) {
        bitcoin = newAddress;
    }

    function setEthereum(string memory newAddress) public onlyBy(owner) {
        ethereum = newAddress;
    }
}
