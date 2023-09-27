import React from "react";
import BookIcon from '@mui/icons-material/Book';
import LibraryBooksIcon from '@mui/icons-material/LibraryBooks';
import GroupsIcon from '@mui/icons-material/Groups';
import LocalLibraryIcon from '@mui/icons-material/LocalLibrary';
import QuestionMarkIcon from '@mui/icons-material/QuestionMark';
import ThumbDownIcon from '@mui/icons-material/ThumbDown';
import HomeIcon from '@mui/icons-material/Home';
import LogoutIcon from '@mui/icons-material/Logout';

export const LeftNavItems = [
    {
        title: 'Home',
        link: '/home',
        icon: <HomeIcon />
    },
    {
        title: 'Add Books',
        link: '/add-book',
        icon: <BookIcon />
    },
    {
        title: 'View Books',
        link: '/view-book',
        icon: <LibraryBooksIcon />
    },
    {
        title: 'View Members',
        link: '/view-members',
        icon: <GroupsIcon />
    },
    {
        title: 'Issue Books',
        link: '/issue-books',
        icon: <LocalLibraryIcon />
    },
    {
        title: 'Issued Status',
        link: '/issued-status',
        icon: <QuestionMarkIcon />
    },
    {
        title: 'Defaulters',
        link: '/defaulter-list',
        icon: <ThumbDownIcon />
    },
    {
        title: 'Logout',
        link: '/',
        icon: <LogoutIcon/>
    }
]