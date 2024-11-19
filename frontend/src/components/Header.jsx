import React, { useState } from "react";
import { HiUser } from "react-icons/hi";
import { MenuIcon, MenuDrower } from "./MenuIcon";
import Avatar from "@mui/material/Avatar";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import EditIcon from "@mui/icons-material/Edit";
import ListItemIcon from "@mui/material/ListItemIcon";
import Divider from "@mui/material/Divider";
import IconButton from "@mui/material/IconButton";
import Tooltip from "@mui/material/Tooltip";
import Logout from "@mui/icons-material/Logout";
import ShoppingCartIcon from "@mui/icons-material/ShoppingCart";
import ReceiptLongIcon from "@mui/icons-material/ReceiptLong";
import Badge from "@mui/material/Badge";
import styled from "@mui/system/styled";
import { Link } from "react-router-dom";

const StyledBadge = styled(Badge)(({ theme }) => ({
  "& .MuiBadge-badge": {
    right: -3,
    top: 13,
    border: `2px solid `,
    padding: "0 4px",
  },
}));

function MaryemaHeader() {
  return (
    <div className="flex flex-1 justify-start max-w-fit h-full p-2">
      <Link to="/" className="flex items-center">
        <h1 className="font-paprika font-bold text-2xl text-gray-700">
          Maryema
        </h1>
      </Link>
    </div>
  );
}

function OtherIcons() {
  const [anchorEl, setAnchorEl] = React.useState(null);
  const open = Boolean(anchorEl);
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
  return (
    <div className="flex flex-1 items-center justify-between max-w-fit mr-6">
      <Tooltip title="Account settings">
        <IconButton
          onClick={handleClick}
          size="small"
          aria-controls={open ? "account-menu" : undefined}
          aria-haspopup="true"
          aria-expanded={open ? "true" : undefined}
        >
          <Avatar alt="user icon" sx={{ width: 32, height: 32 }}>
            <HiUser className="flex-shrink-0 h-7 w-7" />
          </Avatar>
        </IconButton>
      </Tooltip>
      <Tooltip title="Open cart">
        <IconButton aria-label="cart">
          <StyledBadge badgeContent={1} color="error">
            <ShoppingCartIcon />
          </StyledBadge>
        </IconButton>
      </Tooltip>
      <Menu
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        onClick={handleClose}
        slotProps={{
          paper: {
            elevation: 0,
            sx: {
              overflow: "visible",
              filter: "drop-shadow(0px 2px 8px rgba(0,0,0,0.32))",
              mt: 1.5,
              width: 180,
              "& .MuiAvatar-root": {
                width: 32,
                height: 32,
                ml: -0.5,
                mr: 1,
              },
              "&::before": {
                content: '""',
                display: "block",
                position: "absolute",
                top: 0,
                right: 14,
                width: 10,
                height: 10,
                bgcolor: "background.paper",
                transform: "translateY(-50%) rotate(45deg)",
                zIndex: 0,
              },
            },
          },
        }}
        transformOrigin={{ horizontal: "right", vertical: "top" }}
        anchorOrigin={{ horizontal: "right", vertical: "bottom" }}
      >
        <MenuItem onClick={handleClose}>
          <ListItemIcon>
            <ShoppingCartIcon fontSize="small" />
          </ListItemIcon>
          Open cart
        </MenuItem>
        <MenuItem onClick={handleClose}>
          <ListItemIcon>
            <ReceiptLongIcon fontSize="small" />
          </ListItemIcon>
          Orders
        </MenuItem>
        <Divider />
        <MenuItem onClick={handleClose}>
          <Link to="/profile">
            <ListItemIcon>
              <EditIcon fontSize="small" />
            </ListItemIcon>
            Profile
          </Link>
        </MenuItem>
        <MenuItem onClick={handleClose}>
          <ListItemIcon>
            <Logout fontSize="small" />
          </ListItemIcon>
          Logout
        </MenuItem>
      </Menu>
    </div>
  );
}

export default function Header() {
  const [isMenuChecked, setIsMenuChecked] = useState(false);

  const toggleMenu = () => setIsMenuChecked((prev) => !prev);

  return (
    <header className="sticky top-0 z-10 h-full bg-white">
      <nav aria-label="header" className="mx-auto max-w-7xl h-full">
        <div className="flex flex-1 items-center justify-between h-full border-b p-3 border-gray-200 pb-1">
          <MenuIcon isChecked={isMenuChecked} onToggle={toggleMenu} />
          <MaryemaHeader />
          <MenuDrower isVisible={isMenuChecked} />
          <OtherIcons />
        </div>
      </nav>
    </header>
  );
}
