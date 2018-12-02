import * as React from 'react'
import {ReactElement} from "react";

export interface IIcons {
    [name: string] : ReactElement<SVGElement>
}

/**
 * Store the svg element of the icon or image here. The key will be referenced by the iconName property. eg. <IconComponent iconName={key}/>
 */
export const ICONS: IIcons  = {
    logo: <svg className="logo" id="IconLogo" width="100%" height="100%" viewBox="0 0 34 40" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient x1="100%" y1="143.962%" x2="0%" y2="143.962%" id="a">
                <stop stopColor="#65B5F0" stopOpacity="0" offset="0%"/>
                <stop stopColor="#357EDD" offset="100%"/>
            </linearGradient>
        </defs>
        <g fill="none" fillRule="evenodd">
            <path fill="#FFF" d="M3 3h29v34H3z"/>
            <path
                d="M24 21.783v1.567a.89.89 0 0 1-.232.61c-.154.174-.309.261-.463.261H7.695c-.154 0-.309-.087-.463-.261A.89.89 0 0 1 7 23.35v-1.567c0-.29.077-.464.232-.522.154-.174.309-.261.463-.261h15.61c.154 0 .309.087.463.261.155.058.232.232.232.522zM17 9.783v1.567c0 .233-.045.436-.136.61-.091.174-.182.261-.273.261H7.409c-.09 0-.182-.087-.273-.261A1.299 1.299 0 0 1 7 11.35V9.783c0-.29.045-.464.136-.522.091-.174.182-.261.273-.261h9.182c.09 0 .182.087.273.261.09.058.136.232.136.522zM26.48 27.783v1.654c0 .175-.09.349-.266.523-.178.174-.355.261-.532.261H7.797c-.177 0-.354-.087-.531-.261-.177-.174-.266-.348-.266-.523v-1.654c0-.232.089-.406.266-.522.177-.174.354-.261.53-.261h17.886c.177 0 .354.087.532.261.177.116.265.29.265.522zM21 15.783v1.655a.882.882 0 0 1-.19.522c-.128.174-.255.261-.383.261H7.573c-.128 0-.255-.087-.382-.261A.882.882 0 0 1 7 17.437v-1.654c0-.232.064-.406.19-.522.128-.174.255-.261.383-.261h12.854c.128 0 .255.087.382.261.127.116.191.29.191.522z"
                fill="url(#a)"/>
            <rect stroke="#357EDD" strokeWidth="3" x="2.5" y="2.5" width="29" height="35" rx="4"/>
        </g>
    </svg>
};

export interface IIconComponent {
    iconName: string;
}

/**
 * Resolves an SVG by referencing the iconName property with the ICONS object.
 */
export class IconComponent extends React.Component {

    constructor(public props: IIconComponent) {
        super(props);
    }

    public render(): ReactElement<HTMLDivElement> {
        const svg = ICONS[this.props.iconName];
        return(
            <div className={ "icon-wrapper " + this.props.iconName }>
                {svg}
            </div>
        );
    }
}
