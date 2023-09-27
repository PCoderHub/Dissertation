import HomeIcon from '@mui/icons-material/Home';
import LibraryBooksIcon from '@mui/icons-material/LibraryBooks';
import LocalLibraryIcon from '@mui/icons-material/LocalLibrary';
import CurrencyPoundIcon from '@mui/icons-material/CurrencyPound';
import LogoutIcon from '@mui/icons-material/Logout';

export const LeftNavUser = [
    {
        title: 'Home',
        link: '/home',
        icon: <HomeIcon />
    },
    {
        title: 'Available Now',
        link: '/view-book',
        icon: <LibraryBooksIcon />
    },
    {
        title: 'Borrowed books',
        link: '/borrowed',
        icon: <LocalLibraryIcon/>
    },
    {
        title: 'Dues',
        link: '/fine',
        icon: <CurrencyPoundIcon/>
    },
    {
        title: 'Logout',
        link: '/',
        icon: <LogoutIcon/>
    }
];