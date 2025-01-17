// SPDX-License-Identifier: MIT

pragma solidity ^0.8.10;

interface IRewardDistributor {
    struct Claim {
        bytes32 identifier;
        address account;
        uint256 amount;
        bytes32[] merkleProof;
    }
    event RewardClaimed(bytes32 indexed identifier, address indexed token, address indexed account, uint256 amount, uint256 updateCount);
    event RewardMetadataUpdated(bytes32 indexed identifier, address indexed token, bytes32 merkleRoot, bytes32 proof, uint256 indexed updateCount);
    event RoleAdminChanged(bytes32 indexed role, bytes32 indexed previousAdminRole, bytes32 indexed newAdminRole);
    event RoleGranted(bytes32 indexed role, address indexed account, address indexed sender);
    event RoleRevoked(bytes32 indexed role, address indexed account, address indexed sender);

    function BRIBE_VAULT() view external returns (address);
    function DEFAULT_ADMIN_ROLE() view external returns (bytes32);
    function claim(Claim[] memory _claims) external;
    function claimed(bytes32, address) view external returns (uint256);
    function getRoleAdmin(bytes32 role) view external returns (bytes32);
    function grantRole(bytes32 role, address account) external;
    function hasRole(bytes32 role, address account) view external returns (bool);
    function renounceRole(bytes32 role, address account) external;
    function revokeRole(bytes32 role, address account) external;
    function rewards(bytes32) view external returns (address token, bytes32 merkleRoot, bytes32 proof, uint256 updateCount);
    function supportsInterface(bytes4 interfaceId) view external returns (bool);
    function updateRewardsMetadata(Claim[] memory _distributions) external;
}

