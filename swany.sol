pragma solidity =0.8.25;

contract MessageContract {
    string private message;
    constructor(){}
    function writeMessage(string calldata newMessage) public {
        message = newMessage;
    }

    function readMessage() public view returns (string memory) {
        return message;
    }
}