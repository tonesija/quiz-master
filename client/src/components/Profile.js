import React, { useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";

const Profile = () => {
  const { user, isAuthenticated, getAccessTokenSilently } = useAuth0();

  if (isAuthenticated) {
    getAccessTokenSilently().then((accessToken) => {
      console.log(accessToken);
    });
  }

  if (user) {
    return (
      <div className="max-w-sm rounded overflow-hidden shadow-lg mx-6 my-6 px-6 py-4">
        <img
          className="w-half"
          src={user["picture"]}
          alt="Sunset in the mountains"
        />

        <div className="px-6 py-4">
          <div className="font-bold text-xl mb-2">{user["nickname"]}</div>
          <p className="text-gray-700 text-base">
            Lorem ipsum dolor, sit amet consectetur adipisicing elit. Odio quae
            fuga natus explicabo. Minus illum eveniet, vel aliquam temporibus
            perspiciatis libero iusto sint eligendi quos, minima facere
            doloribus quod exercitationem.
          </p>
        </div>
        <div className="px-6 pt-4 pb-2">
          <span className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">
            #photography
          </span>
          <span className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">
            #travel
          </span>
          <span className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2">
            #winter
          </span>
        </div>
      </div>
    );
  } else {
    return (
      <svg className="animate-spin max-w-sm" height={100} width={100}>
        <path d="M0,50 a1,1 0 0,0 100,0" fill="blue" />
      </svg>
    );
  }
};

export default Profile;
