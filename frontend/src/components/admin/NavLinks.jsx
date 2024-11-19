import HomeIcon from "@mui/icons-material/Home";
import { NavLink } from "react-router-dom";
import PeopleAltIcon from "@mui/icons-material/PeopleAlt";
import SettingsIcon from "@mui/icons-material/Settings";
import ShoppingCartIcon from "@mui/icons-material/ShoppingCart";
import InventoryIcon from "@mui/icons-material/Inventory";

const links = [
  {
    name: "Dashboard",
    to: "/admin",
    icon: <HomeIcon />,
    end: true,
  },
  {
    name: "Products",
    to: "/admin/products",
    icon: <InventoryIcon />,
  },
  {
    name: "Orders",
    to: "/admin/orders",
    icon: <ShoppingCartIcon />,
  },
  {
    name: "Customers",
    to: "/admin/customers",
    icon: <PeopleAltIcon />,
  },
  {
    name: "Settings",
    to: "/admin/settings",
    icon: <SettingsIcon />,
  },
];

export default function NavLinks() {
  return (
    <>
      {links.map((link) => {
        return (
          <NavLink
            key={link.name}
            to={link.to}
            end={link.end}
            className={({ isActive }) =>
              `flex h-[48px] grow items-center justify-center gap-2 rounded-md bg-gray-50 p-3 text-sm font-medium hover:bg-sky-100 hover:text-blue-600 md:flex-none md:justify-start md:p-2 md:px-3 ${
                isActive && "bg-sky-100 text-blue-600"
              }`
            }
          >
            {link.icon}
            <p className="hidden md:block">{link.name}</p>
          </NavLink>
        );
      })}
    </>
  );
}
