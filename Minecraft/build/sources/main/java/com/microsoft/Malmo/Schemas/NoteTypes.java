//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, v2.2.4 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2021.11.10 at 11:44:37 PM EST 
//


package com.microsoft.Malmo.Schemas;

import javax.xml.bind.annotation.XmlEnum;
import javax.xml.bind.annotation.XmlEnumValue;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for NoteTypes.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * <p>
 * <pre>
 * &lt;simpleType name="NoteTypes">
 *   &lt;restriction base="{http://www.w3.org/2001/XMLSchema}string">
 *     &lt;enumeration value="F_sharp_3"/>
 *     &lt;enumeration value="G3"/>
 *     &lt;enumeration value="G_sharp_3"/>
 *     &lt;enumeration value="A3"/>
 *     &lt;enumeration value="A_sharp_3"/>
 *     &lt;enumeration value="B3"/>
 *     &lt;enumeration value="C4"/>
 *     &lt;enumeration value="C_sharp_4"/>
 *     &lt;enumeration value="D4"/>
 *     &lt;enumeration value="D_sharp_4"/>
 *     &lt;enumeration value="E4"/>
 *     &lt;enumeration value="F4"/>
 *     &lt;enumeration value="F_sharp_4"/>
 *     &lt;enumeration value="G4"/>
 *     &lt;enumeration value="G_sharp_4"/>
 *     &lt;enumeration value="A4"/>
 *     &lt;enumeration value="A_sharp_4"/>
 *     &lt;enumeration value="B4"/>
 *     &lt;enumeration value="C5"/>
 *     &lt;enumeration value="C_sharp_5"/>
 *     &lt;enumeration value="D5"/>
 *     &lt;enumeration value="D_sharp_5"/>
 *     &lt;enumeration value="E5"/>
 *     &lt;enumeration value="F5"/>
 *     &lt;enumeration value="F_sharp_5"/>
 *   &lt;/restriction>
 * &lt;/simpleType>
 * </pre>
 * 
 */
@XmlType(name = "NoteTypes")
@XmlEnum
public enum NoteTypes {

    @XmlEnumValue("F_sharp_3")
    F_SHARP_3("F_sharp_3"),
    @XmlEnumValue("G3")
    G_3("G3"),
    @XmlEnumValue("G_sharp_3")
    G_SHARP_3("G_sharp_3"),
    @XmlEnumValue("A3")
    A_3("A3"),
    @XmlEnumValue("A_sharp_3")
    A_SHARP_3("A_sharp_3"),
    @XmlEnumValue("B3")
    B_3("B3"),
    @XmlEnumValue("C4")
    C_4("C4"),
    @XmlEnumValue("C_sharp_4")
    C_SHARP_4("C_sharp_4"),
    @XmlEnumValue("D4")
    D_4("D4"),
    @XmlEnumValue("D_sharp_4")
    D_SHARP_4("D_sharp_4"),
    @XmlEnumValue("E4")
    E_4("E4"),
    @XmlEnumValue("F4")
    F_4("F4"),
    @XmlEnumValue("F_sharp_4")
    F_SHARP_4("F_sharp_4"),
    @XmlEnumValue("G4")
    G_4("G4"),
    @XmlEnumValue("G_sharp_4")
    G_SHARP_4("G_sharp_4"),
    @XmlEnumValue("A4")
    A_4("A4"),
    @XmlEnumValue("A_sharp_4")
    A_SHARP_4("A_sharp_4"),
    @XmlEnumValue("B4")
    B_4("B4"),
    @XmlEnumValue("C5")
    C_5("C5"),
    @XmlEnumValue("C_sharp_5")
    C_SHARP_5("C_sharp_5"),
    @XmlEnumValue("D5")
    D_5("D5"),
    @XmlEnumValue("D_sharp_5")
    D_SHARP_5("D_sharp_5"),
    @XmlEnumValue("E5")
    E_5("E5"),
    @XmlEnumValue("F5")
    F_5("F5"),
    @XmlEnumValue("F_sharp_5")
    F_SHARP_5("F_sharp_5");
    private final String value;

    NoteTypes(String v) {
        value = v;
    }

    public String value() {
        return value;
    }

    public static NoteTypes fromValue(String v) {
        for (NoteTypes c: NoteTypes.values()) {
            if (c.value.equals(v)) {
                return c;
            }
        }
        throw new IllegalArgumentException(v);
    }

}
